import os
import csv
from src.insta_bot import *
from  multiprocessing import Process

def run_choice1(user, total, interval):
    bot = InstaBot(user[0], user[1])
    bot.follow_by_explore(total, interval)
    return(bot)

def run_choice2(user, total, interval, hashtags):
    bot = InstaBot(user[0], user[1])
    bot.follow_by_hashtag(total, interval, hashtags)
    return(bot)

def run_choice3(user, total, interval, hashtags):
    bot = InstaBot(user[0], user[1])
    bot.likes_by_hashtag(total, interval, hashtags)
    return(bot)

def run_choice4(user, total):
    bot = InstaBot(user[0], user[1])
    bot.unfollow(total)
    return(bot)

def options():
    choices = [1,2,3,4]
    print('Select what you want to do:')
    print('1. Follow people based on your explore')
    print('2. Follow people using hashtags you want')
    print('3. Likes on posts using hashtags you want')
    print('4. Unfollow')
    choice = int(input('Insert here: '))

    while(choice not in choices):

        print('Sorry, option not found... Try again')
        print('1. Follow people based on your explore')
        print('2. Follow people using hashtags you want')
        print('3. Likes on posts using hashtags you want')
        print('4. Unfollow')
        choice = int(input('Insert here: '))

    return(choice)

if __name__=='__main__':

    print('Welcome to InstaBot!')
    file = str(input('Insert the secret file you want to read: '))
    list_of_files = list(os.listdir('secret/'))

    if(file in list_of_files):

        with open('secret/{}'.format(file), newline='') as csvfile:
            reader = csv.reader(csvfile)
            users = list(reader)

        choice = options()
        
        if(choice==1):
            print('Insert the requested paramaters below')
            total = int(input('Total to follow: '))
            interval = int(input('Interval in minutes (recommended 5): '))

            for user in users:
                print('user: {}'.format(user[0]))
                p = Process(target=run_choice1, args=(user, total, interval))
                p.start()

        elif(choice==2):
            print('Insert the requested paramaters below')
            total = int(input('Total to follow: '))
            interval = int(input('Interval in minutes (recommended 5): '))
            hashtags = [str(hashtag) for hashtag in input('Insert your hashtags: ').split()]

            for user in users:
                print('user: {}'.format(user[0]))
                p = Process(target=run_choice2, args=(user, total, interval, hashtags))
                p.start()
                
        elif(choice==3):
            print('Insert the requested paramaters below')
            total = int(input('Total to follow: '))
            interval = int(input('Interval in minutes (recommended 5): '))
            hashtags = [str(hashtag) for hashtag in input('Insert your hashtags: ').split()]

            for user in users:
                print('user: {}'.format(user[0]))
                p = Process(target=run_choice3, args=(user, total, interval, hashtags))
                p.start()

        elif(choice==4):
            print('Insert the requested paramaters below')
            total = int(input('Total to unfollow: '))

            for user in users:
                print('user: {}'.format(user[0]))
                p = Process(target=run_choice4, args=(user, total))
                p.start()
    else:
        print('Some error has ocurred.')
        print('Try create a new .csv file in the secret folder.')