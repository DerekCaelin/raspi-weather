
![mounted pi](https://cdn.mastodon.technology/media_attachments/files/106/046/825/640/444/026/original/65a693504c9764e6.jpg)

# raspi-weather
a weather application for the raspberry pi and the Inky pHAT (https://shop.pimoroni.com/products/inky-phat?variant=12549254217811)

The script displays:
- the current temperature
- today's date
- today's temperature range
- tomorrow's temperature range
- a verbal description of today's weather
- weather icons drawn with math and python's drawing library

A valueable resource: https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat

## Installation

### SSH into your rasberry pi
> ssh pi@[IPADDRESS]

### Install the Inky pHAT libraries
> curl https://get.pimoroni.com/inky | bash

### Copy weather.py over to your pi
> scp /path/to/file username@a:/path/to/destination

### Obtain a Weather Underground account
https://www.wunderground.com/

### Edit weather.py and update the variables with your API Key, the closest station, and your zipcode
- ZIPCODE

- STATION

- APIKEY

### Set the raspberru pi to run your script every 30 minutes
> crontab -e

At the very bottom of your crontab file, add the following line:

> */30 * * * * python3 /[PATH TO YOUR SCRIPT]

