import tweepy
import requests
import schedule 
import time    
from win10toast import ToastNotifier
import random
from datetime import datetime, timedelta
import os
import datetime

def get_elapsed_time(start_time):
    current_time = datetime.datetime.now()
    elapsed_time = current_time - start_time
    return elapsed_time.total_seconds() / 3600  # Convert elapsed time to hours

def save_timestamp(start_time):
    with open("timestamp.txt", "w") as file:
        file.write(str(start_time))

def load_timestamp():
    if os.path.exists("timestamp.txt"):
        with open("timestamp.txt", "r") as file:
            start_time = datetime.datetime.fromisoformat(file.read())
    else:
        start_time = datetime.datetime.now()
        save_timestamp(start_time)
    return start_time

def notify(notification):
    # do this stuff when the script exits
    # send notification to the user
    toast = ToastNotifier()
    toast.show_toast("Programming Quotes Bot", notification, duration=10)

    return

# request data from the API
def get_data():
    url = "https://zenquotes.io/api/random"
    response = requests.get(url)
    data = response.json()
    return data

# Bot to automatically tweet
access_granted = False
def tweet():
    # Authenticate to Twitter
    import json

    # Open the JSON file
    with open('keys.json', 'r') as json_file:
        data = json.load(json_file)
        access_token = data["access_token"]
        access_token_secret = data["access_token_secret"]
        api_key = data["api_key"]
        api_secret = data["api_secret"]
        Bearer_token = data["Bearer_token"]

    # Create the api object
    client = tweepy.Client(Bearer_token,api_key,api_secret,access_token,access_token_secret)
    auth = tweepy.OAuth1UserHandler(api_key,api_secret,access_token,access_token_secret)
    # auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    try:
        api.verify_credentials()
        access_granted = True
        print("Authentication OK")
    except Exception as e:
        access_granted = False
        print("Error during authentication: " + str(e))

    if access_granted:
        try:
            
            data = get_data()
            quote = data[0]["q"]
            author = data[0]["a"]
            tags = ["#quotes", "#programming","#CodeNewbies","#100DaysOfCode","#30DaysOfFlutter","#javascript", "#inspire", "#inspiration","#python","#java","#c"]
            new_tags = random.sample(tags, 3)
            message = quote + "\n -" + author + "\n" + " ".join(new_tags)
            client.create_tweet(text = message)
            # api.update_status(status=message)
        except Exception as e:
            error_log = open("error_log.txt", "wt")
            error_log.write(str(e))
            error_log.close()
            notify("Error!! ")

if __name__ == "__main__":
    notify("Starting script...")

    while True:
        start_time = load_timestamp()
        elapsed_time = get_elapsed_time(start_time)
    
        if elapsed_time > 5:
            notify("Posting tweet...")
            tweet()
            time.sleep(10)  # Simulating the script's execution time
        
            save_timestamp(datetime.datetime.now())  
        else:
            continue