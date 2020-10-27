import re
import time
import requests
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class InstaBot():

    def __init__(self, username: str, password: str):

        #urls
        self.base = 'https://www.instagram.com/'
        self.profile = self.base + username
        self.direct = self.base + 'direct/inbox/'
        self.explore = self.base + 'explore/'
        self.activity = self.base + 'accounts/activity/'
        self.suggested = self.base + 'explore/people/suggested/'
        self.hashtag = self.base + 'explore/tags/' # + hashtag

        #xpaths 
        self.first_post_explore = '/html/body/div[1]/section/main/div/div[1]/div/div[1]/div[2]/div'
        self.and_others = '/html/body/div[4]/div[2]/div/article/div[3]/section[2]/div/div[2]/button'
        
        self.username = username
        self.sleep_time = 5

        #webdriver
        ops = webdriver.FirefoxOptions()
        ops.add_argument('--headless')
        self.browser = webdriver.Firefox(executable_path=PATH_TO_YOUR_WEBDRIVER_HERE, options=ops)

        #login
        self.browser.get(self.base)
        time.sleep(self.sleep_time)

        self.browser.find_element_by_xpath("//input[@name=\'username\']")\
            .send_keys(username)
        self.browser.find_element_by_xpath("//input[@name=\'password\']")\
            .send_keys(password)
        self.browser.find_element_by_xpath("//button[@type='submit']")\
            .click()
        
        time.sleep(self.sleep_time)

        #maybe you want to change 'Agora não' by 'Not Now'
        self.browser.find_element_by_xpath("//button[contains(text(), 'Agora não')]")\ 
            .click()

    def go_to_profile(self):
        self.browser.get(self.profile)
        time.sleep(self.sleep_time)

    def get_followers(self):
        self.go_to_profile()
        self.browser.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[2]/a')\
            .click()
        time.sleep(self.sleep_time)
        element = self.browser.find_element_by_xpath('/html/body/div[4]/div/div')
        self.browser.execute_script("arguments[0].scrollIntoView(true);", element)

    def follow_person_post(self, follows_per_post: int = 6):

        for follow_id in range(1, follows_per_post):

            person_to_follow = '/html/body/div[5]/div/div/div[2]/div/div/div['+str(follow_id)+']/div[3]/button'

            self.browser.find_element_by_xpath(person_to_follow)\
                .click()
            time.sleep(self.sleep_time)

    def follow_by_explore(self, total: int, interval: int):
        interval = interval * 60
        new_followers = 0
        
        while(new_followers < total):

            self.browser.get(self.explore)
            time.sleep(self.sleep_time)

            try:
                self.browser.find_element_by_xpath(self.first_post_explore)\
                    .click()
                time.sleep(self.sleep_time)
                
                self.browser.find_element_by_xpath(self.and_others)\
                    .click()
                time.sleep(self.sleep_time)

                self.follow_person_post()
                new_followers += 5
                time.sleep(interval)
                
                print('Total: {}, Followed: {}'.format(total, new_followers))
                
            except:
                print('Some error has ocurred.')
                time.sleep(self.sleep_time)
        
        print('Task Finished.')
        self.browser.quit()

    def get_url_data_hashtags(self, hashtag):
        response = requests.get('https://www.instagram.com/explore/tags/' + hashtag + '/')
        return response

    def get_shortcodes(self, response):
        result = re.finditer('shortcode', response.text)
        indices = [m.start(0) for m in result]
        shortcodes = []
        for indice in indices:
            shortcode = response.text[indice + len('shortcode":"'):indice + len('shorcode":"CESgfh4BefM"')]
            shortcodes.append(shortcode)
        return shortcodes

    def follow_by_hashtag(self, total: int, interval: int, hashtags: list, follow_per_post: int=6):
        #self.browser.get('https://www.instagram.com/explore/')
        button = '/html/body/div[1]/section/main/div/div[1]/article/div[3]/section[2]/div/div[2]/button'
        
        new_followers = 0
        interval = interval * 60
        total_hashtags = int(len(hashtags))
        hashtag_division = int(total/total_hashtags)

        #get posts url by hashtags respecting hashtag division
        posts_url = []

        for hashtag in hashtags:
            response = self.get_url_data_hashtags(hashtag)
            shortcodes = self.get_shortcodes(response)
            shortcodes[0:hashtag_division]
            for shortcode in shortcodes:
                post_url = 'https://www.instagram.com/p/' + shortcode + '/'
                posts_url.append(post_url)
        
        while(new_followers < total):
            
            for post_url in posts_url:
                #following people
                try:
                    print('Post url: {}'.format(post_url))
                    self.browser.get(post_url)
                    time.sleep(self.sleep_time)
                    self.browser.find_element_by_xpath(button).click()
                    time.sleep(self.sleep_time)

                    for person in range(1, follow_per_post):
                        print('Person ID: {}'.format(person))
                        follow_button = '/html/body/div[4]/div/div/div[2]/div/div/div[' + str(person) + ']/div[3]/button'
                        self.browser.find_element_by_xpath(follow_button).click()
                        time.sleep(self.sleep_time)
                        new_followers += 1
                        print('Current Follows {}. Expected: {}'.format(new_followers, total))
                    #giant sleep
                    time.sleep(interval)
                except:
                    print('Button "And Others" not found...')
        
        print('Task Finished!')

    def likes_by_hashtag(self, total: int, interval: int, hashtags: list):

        interval = interval * 60

        for hashtag in hashtags:

            base_url = 'https://www.instagram.com/explore/tags/' + hashtag
            self.browser.get(base_url)
            time.sleep(self.sleep_time)

            self.browser.find_element_by_xpath('/html/body/div[1]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')\
                .click()
            time.sleep(self.sleep_time)

            self.browser.find_element_by_xpath(self.and_others)\
                .click()
            time.sleep(self.sleep_time)

            self.follow_person_post()

            time.sleep(interval)
        print('Task Finished.')
        self.browser.quit()

    def unfollow(self, quantity: int):
        
        unfollows = 0
        while(unfollows < quantity):
            
            self.go_to_profile()
            time.sleep(5)
            self.browser.find_element_by_xpath("//a[contains(@href, '/following')]")\
                .click()
            time.sleep(5)
                
            try:
                #may you want to change 'Seguindo' by 'Following'
                self.browser.find_element_by_xpath("//button[contains(text(), 'Seguindo')]")\
                    .click()
                time.sleep(5)
                #may you want to change 'Deixar de seguir' by 'Unfollow'
                self.browser.find_element_by_xpath("//button[contains(text(), 'Deixar de seguir')]")\
                    .click()
                time.sleep(5)
                unfollows += 1

            except:
                print('Error while trying to click button to unfollow.')
            
            print('Total: {}, unfollows: {}'.format(quantity, unfollows))
            time.sleep(5)
                
        print('Task Finished.')
        self.browser.quit()
