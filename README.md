# Instagram collector

This simple python 3 script continuously downloads images and videos from Instagram, based on a list of user names and/or a list of tags. Every N seconds, the script checks if new pictures or videos have been uploaded by those users or with those tags. The script was created to collect images from an event while it is happening.

## Dependencies
The script uses the [Requests](http://docs.python-requests.org/en/latest/) module:

	pip3 install requests

## Configuration
The script is accompanied by a `config.ini` file. This repository only contains an example file. Copy it and update it with your own settings.

Setting | Description
--------|------------
instagram_client_id | This should contain a valid Instagram client id, easily retrieved from http://instagram.com/developer/clients/manage/.
sleeptime | How long should the script wait until it checks to see if there are new files available
users | A comma seperated list of user names.
tags | A comma seperated list of tags.

## Usage
Just run the script from the command line:

	python3 collector.py

