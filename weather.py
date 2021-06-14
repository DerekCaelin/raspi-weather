from inky import InkyPHAT
import json
import requests

inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)

from PIL import Image, ImageFont, ImageDraw

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

#fonts
from font_fredoka_one import FredokaOne
font = ImageFont.truetype(FredokaOne, 22)
font2 = ImageFont.truetype(FredokaOne, 14)
fontBIG = ImageFont.truetype(FredokaOne, 34)
fontSML = ImageFont.truetype(FredokaOne, 10)

APIKEY = #insert API key from https://www.wunderground.com/member/api-keys after registering an account
STATION = #insert station ID from https://www.wunderground.com/
ZIPCODE = #insert Zip Code  

#get current conditions from weather underground
query = "https://api.weather.com/v2/pws/observations/current?stationId="+STATION+"&format=json&units=e&apiKey="+APIKEY
url = requests.get(query)
text = url.text
x = json.loads(text)

#get 5-day json from weather underground
wquery = "https://api.weather.com/v3/wx/forecast/daily/5day?postalKey="+ZIPCODE+":US&units=e&language=en-US&format=json&apiKey="+APIKEY
wurl = requests.get(wquery)
wtext = wurl.text
y = json.loads(wtext)

#get variables from jsons
#print(x['observations'][0]['imperial']['temp'])
currentTemp = x['observations'][0]['imperial']['temp']
currentDate = x['observations'][0]['obsTimeLocal'].split(' ')[0].split('-',1)[1]
calendarDayTemperatureMax = y['calendarDayTemperatureMax']
calendarDayTemperatureMin = y['calendarDayTemperatureMin']
tomorrowMax = y['calendarDayTemperatureMax'][1]
tomorrowMin = y['calendarDayTemperatureMin'][1]
narrative = y['narrative'][0]
narrative = narrative.replace('the ','').split(". ")
dayOfWeek = y['dayOfWeek'][1]

# get icon
icon = y['daypart'][0]['iconCode'][0]
if icon is None: #in the evenings the first response in the array is null 
	icon = y['daypart'][0]['iconCode'][1]
#icon = 41

#make message
nowTemp = str(currentTemp) + " " + u"\N{DEGREE SIGN}" + "F"
rangeMessage = str(calendarDayTemperatureMin[0]) + "-" + str(calendarDayTemperatureMax[0]) +" "+ u"\N{DEGREE SIGN}"  +"F"
futureMessage = str(tomorrowMin) + "-" + str(tomorrowMax) + " " + u"\N{DEGREE SIGN}"  + "F"

#draw the standard stuff
draw.rectangle((0,0,212,104),inky_display.BLACK)

draw.line((0,0,115,115),inky_display.RED, width=30) 
draw.text((5, 5), nowTemp, inky_display.WHITE, font)
draw.text((5, 30), "Today: "+rangeMessage, inky_display.WHITE, font2)
draw.text((5, 46), dayOfWeek +": " + futureMessage, inky_display.WHITE, font2)
#draw.text((5, 75), narrative[0], inky_display.WHITE, font2)
# Start Variable Font Size and wrapping for Narrative
y_top = 60		# Top of the narrative area
y_bottom = 100		# Bottom of the narrative area
fontSize = 9  		# Starting Font Size
fontMaxSize = 30	# Maximum font size

fontNAR = ImageFont.truetype(FredokaOne,fontSize)
while (fontNAR.getsize(narrative[0])[0] <= int(inky_display.width * .95)) and (fontSize < fontMaxSize):
	# iterate until the text size is just larger than the criteria
	fontSize += 1
	fontNAR = ImageFont.truetype(FredokaOne, fontSize)
fontSize -= 1
fontNAR = ImageFont.truetype(FredokaOne,fontSize)
narrative_w, narrative_h = fontNAR.getsize(narrative[0])
narrative_x = int((inky_display.width - narrative_w) / 2)
narrative_y = int(y_top + ((y_bottom - y_top - narrative_h) / 2))
draw.text((narrative_x, narrative_y), narrative[0], inky_display.WHITE, fontNAR)
# End Variable Font Size for Narrative

#date
w, h = font.getsize(currentDate)
x = (inky_display.WIDTH / 2) - (w / 2)
draw.text((x+15,5), currentDate, inky_display.WHITE, font2)

# Make your own icons to align with weather undergrounds icon set: https://ibm.co/TWCICv2

# big moon
if (icon ==  27) or (icon == 29) or (icon == 31) or (icon == 33):
	sx = 135
	sy = 10

	draw.ellipse((sx, sy, sx+50, sy+50), inky_display.WHITE)
	if (icon is 31) or (icon is 33): 
		draw.ellipse((sx+10, sy-10, sx+60, sy+40), inky_display.BLACK) 

# small sun
if (icon == 28) or (icon == 30) or (icon == 38) or (icon == 41):
	sx = 135
	sy = 25
	draw.ellipse((sx, sy, sx+10, sy+10), inky_display.WHITE)
	draw.polygon((sx+1, sy, sx-10, sy+5, sx+10, sy+9), inky_display.WHITE)
	draw.polygon((sx+5, sy-10, sx, sy, sx+10, sy), inky_display.WHITE)
	draw.polygon((sx+10, sy, sx+20, sy+5, sx+10, sy+10), inky_display.WHITE)
	draw.line((sx-5, sy-5, sx+15, sy+15), inky_display.WHITE, 5)
	draw.line((sx-5, sy+15, sx+15, sy-5), inky_display.WHITE, 5)

# big sun!
if (icon == 32) or (icon == 34) or (icon == 36):
	sx = 155
	sy = 25

	# rays                
	draw.polygon((sx+12, sy-16, sx+17, sy,    sx+7 , sy,    sx+12, sy-16), inky_display.WHITE, 5) #top 
	draw.polygon((sx+12, sy+40, sx+17, sy+30, sx+7 , sy+30, sx+12, sy+40), inky_display.WHITE, 5) #down
	draw.polygon((sx-17, sy+12, sx   , sy+7 , sx   , sy+17, sx-16, sy+12), inky_display.WHITE, 5) #left
	draw.polygon((sx+40, sy+12, sx+24, sy+7 , sx+24, sy+17, sx+40, sy+12), inky_display.WHITE, 5) #right

	draw.line((sx-10, sy-10, sx+34, sy+34), inky_display.WHITE, 5)
	draw.line((sx-10, sy+34, sx+34, sy-10), inky_display.WHITE, 5)

	# sun
	draw.ellipse((sx-5, sy-5, sx+29, sy+29), inky_display.BLACK)
	draw.ellipse((sx  , sy  , sx+24, sy+24), inky_display.WHITE)

# secondary "heavy" cloud
if (icon == 27) or (icon == 28) or (icon == 38):
	sx = 170	
	sy = 25

	#black
	draw.ellipse((sx-5, sy-5, sx+20, sy+20), inky_display.BLACK)
	draw.ellipse((sx+5, sy, sx+30, sy+20), inky_display.BLACK)

	#white
	draw.ellipse((sx, sy, sx+15, sy+15), inky_display.WHITE)
	draw.ellipse((sx+10, sy+5, sx+25, sy+15), inky_display.WHITE)

# small cloud
if (icon is 33) or (icon is 34):
	sx = 145
	sy = 35

	#outline
	draw.ellipse((sx-3, sy-3, sx+8, sy+8), inky_display.BLACK)
	draw.ellipse((sx+2, sy-8, sx+18, sy+8), inky_display.BLACK)
	draw.ellipse((sx+7, sy-13,sx+28, sy+8), inky_display.BLACK)
	draw.ellipse((sx+17, sy-8, sx+33, sy+8), inky_display.BLACK)

	#white
	draw.ellipse((sx, sy, sx+5, sy+5), inky_display.WHITE)
	draw.ellipse((sx+5, sy-5, sx+15, sy+5), inky_display.WHITE)
	draw.ellipse((sx+10, sy-10, sx+25, sy+5), inky_display.WHITE)
	draw.ellipse((sx+20, sy-5, sx+30, sy+5), inky_display.WHITE)

# stars = clear night
if (icon == 31):
	sx = 160
	sy = 30
	draw.line((sx, sy, sx+10, sy), inky_display.WHITE, 2)

	sx = 165
	sy = 25
	draw.line((sx, sy, sx, sy+10), inky_display.WHITE, 2)

# if icon has a big cloud
if (icon >= 3 and icon <=14) or (icon >= 16 and icon <= 22) or (icon >= 26 and icon <= 30) or (icon == 35) or (icon >= 38 and icon <= 43) or (icon >= 45):
	sx = 140
	sy = 40

	#dark
	draw.ellipse((sx-5, sy-5, sx+15, sy+15),inky_display.BLACK) 
	draw.ellipse((sx, sy-15, sx+30, sy+15),inky_display.BLACK)
	draw.ellipse((sx+10, sy-25, sx+50, sy+15), inky_display.BLACK)
	draw.ellipse((sx+30, sy-15, sx+60, sy+15), inky_display.BLACK)

	#white
	draw.ellipse((sx, sy, sx+10, sy+10), inky_display.WHITE)
	draw.ellipse((sx+5, sy-10, sx+25, sy+10), inky_display.WHITE)
	draw.ellipse((sx+15, sy-20, sx+45, sy+10), inky_display.WHITE)
	draw.ellipse((sx+35, sy-10, sx+55, sy+10), inky_display.WHITE)

# heavy rain drop
if (icon >= 3 and icon <12):
	sx = 175
	sy = 60
	draw.ellipse((sx, sy, sx+5,sy+5),inky_display.WHITE)
	draw.polygon((sx-5, sy-5, sx, sy+3, sx+5, sy+1, sx-5, sy-5), inky_display.WHITE)
 
# left rain drop
if (icon == 9) or  (icon == 11) or (icon == 12) or (icon == 39) or (icon == 40):
	sx = 160
	sy = 60
	draw.ellipse((sx+3, sy-3, sx+7, sy), inky_display.WHITE)
	draw.polygon((sx, sy-6, sx+5, sy-1, sx+6, sy-4, sx+2, sy-6), inky_display.WHITE) 

# right rain drop
if (icon == 9) or (icon == 11) or (icon == 12) or (icon == 39) or (icon == 40) or (icon == 45):
	sx = 180
	sy = 60
	draw.ellipse((sx+3, sy-4, sx+7, sy-1), inky_display.WHITE)
	draw.polygon((sx, sy-6, sx+5, sy-1, sx+6, sy-4, sx+2, sy-6), inky_display.WHITE)

# right lightning bolt 
if (icon == 3) or (icon == 4):
	sx = 180
	sy = 47
	draw.polygon(((sx+2, sy+6), (sx+10, sy+6), (sx+14, sy+12), (sx+8, sy+12), (sx+10, sy+18), (sx+2, sy+10), (sx+7, sy+10), (sx+2, sy+6)), inky_display.WHITE)

# wind
if (icon >= 23) and (icon <= 25):
	#left cloud
	draw.ellipse((165, 10, 185, 30), inky_display.WHITE) #puff of wind
	draw.line((140, 30, 175, 30), inky_display.WHITE, 5) #line
	draw.ellipse((170, 15, 180, 25), inky_display.BLACK) #negative space ball
	draw.line((140, 25, 175, 25), inky_display.BLACK, 5) #negative space line

	draw.ellipse((175, 35, 195, 55), inky_display.WHITE)
	draw.line((150, 40, 185, 40), inky_display.WHITE, 5)
	draw.ellipse((180, 40, 190, 50), inky_display.BLACK)
	draw.line((150, 45, 185, 45), inky_display.BLACK, 5) 

# big snow below
if (icon == 13):
	draw.text((160, 45), "*", inky_display.WHITE, fontBIG)

# smaller snow
if (icon >= 41) and (icon <= 43):
	draw.text((157, 50), "*", inky_display.WHITE, font2)
	draw.text((175, 53), "*", inky_display.WHITE, font2)
	draw.text((164, 56), "*", inky_display.WHITE, font)

# foggy
if (icon >= 19) and (icon <= 22) :
	draw.line((150, 57, 190, 57), inky_display.WHITE, 3)
	draw.line((154, 61, 162, 61), inky_display.WHITE, 3)
	draw.line((167, 61, 195, 61), inky_display.WHITE, 3)
	draw.line((150, 65, 190, 65), inky_display.WHITE, 3)

inky_display.set_image(img)
inky_display.show()


