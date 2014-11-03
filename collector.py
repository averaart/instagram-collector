from datetime import datetime, timedelta
from time import sleep
import urllib.request
import configparser

import requests


config = configparser.ConfigParser()
config.read('config.ini')

# Retrieving settings from config file
client_id = config['settings']['instagram_client_id']
sleeptime = int(config['settings']['sleeptime'])
date_format = "%Y%m%d%H%M%S"

# Retrieving users and tags from config file
tags = {tag: "0" for tag in filter(bool, [x.strip() for x in config['content']['tags'].split(",")])}
user_names = filter(bool, [x.strip() for x in config['content']['users'].split(",")])

# Convert user names to user IDs
user_ids = set()
for username in user_names:
    user_search_response = requests.get(
        "https://api.instagram.com/v1/users/search?client_id=" + client_id + "&q=" + username)
    user_search_results = user_search_response.json()
    for result in user_search_results['data']:
        if result['username'] == username:
            user_ids.add(result['id'])


# Main loop
while True:

    print("Starting...")
    min_timestamp = str(int((datetime.now() - timedelta(seconds=(sleeptime * 2))).timestamp()))
    max_timestamp = str(int(datetime.now().timestamp()))
    downloads = {}

    # Lookup latest uploads for specific users

    for id in user_ids:
        print("Working on userId [ " + id + " ]")
        user_media_response = requests.get(
            "https://api.instagram.com/v1/users/" + id + "/media/recent?client_id=" + client_id +
            "&min_timestamp=" + min_timestamp + "&max_timestamp=" + max_timestamp)
        user_media = user_media_response.json()

        for result in user_media['data']:
            username = result['user']['username']
            timestamp = int(result['created_time'])
            filename = datetime.fromtimestamp(timestamp).strftime(date_format) + "-" + username
            if result['type'] == 'image':
                image_url = result["images"]['standard_resolution']['url']
                downloads[image_url] = filename + ".jpg"
            elif result['type'] == 'video':
                image_url = result["videos"]['standard_resolution']['url']
                downloads[image_url] = filename + ".mp4"

    # Lookup latest uploads with specific tags

    for tag, min_tag_id in iter(tags.items()):
        print("Working on tag [ " + tag + " ] with min_tag_id [ " + min_tag_id + " ]")

        while True:
            tagged_media_response = requests.get(
                "https://api.instagram.com/v1/tags/" + tag + "/media/recent?client_id=" + client_id + "&min_tag_id=" + min_tag_id)
            tagged_media = tagged_media_response.json()

            for result in tagged_media['data']:
                username = result['user']['username']
                timestamp = int(result['created_time'])
                filename = datetime.fromtimestamp(timestamp).strftime(date_format) + "-" + username
                if result['type'] == 'image':
                    image_url = result["images"]['standard_resolution']['url']
                    downloads[image_url] = filename + ".jpg"
                elif result['type'] == 'video':
                    image_url = result["videos"]['standard_resolution']['url']
                    downloads[image_url] = filename + ".mp4"

            if 'min_tag_id' in tagged_media['pagination'].keys():
                min_tag_id = tagged_media['pagination']['min_tag_id']
                tags[tag] = min_tag_id
            else:
                break

    # Download gathered urls

    for url, filename in downloads.items():
        print("Downloading " + filename)
        urllib.request.urlretrieve(url, filename)

    min_timestamp = max_timestamp
    print("Going to sleep...")
    sleep(sleeptime)
