
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

A valuable resource: https://learn.pimoroni.com/tutorial/sandyj/getting-started-with-inky-phat

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

### Set the raspberry pi to run your script every 30 minutes
> crontab -e

At the very bottom of your crontab file, add the following line:

> */30 * * * * python3 /[PATH TO YOUR SCRIPT]

### MIT License

Copyright (c) 2020 Derek Caelin

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


