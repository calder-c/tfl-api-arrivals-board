import time
import requests
from math import floor
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from threading import Thread
import pygame
import sys


args = [arg for arg in sys.argv[1:]]
if len(args) == 6:
    bus_naptan = args[0]
    route = args[1]
    bus_direction = args[2]
    overground_naptan = args[3]
    overground_direction = args[4]
    interval = int(args[5])
else:
    raise SystemExit(f"Usage: {sys.argv[0]} <bus NAPTAN> <bus route> <bus direction (inbound, outbound)> <overground NAPTAN> <overground direction (inbound, outbound)> <check interval (secs)>")

print(bus_naptan, overground_naptan)
active = False
def getBus(naptan, only=None):
    recv = requests.get("https://api.tfl.gov.uk/StopPoint/" + naptan + "/arrivals" ).json()
    buses = []
    for x in recv:
        if x['direction'] == bus_direction:
            data = {}
            data['mins'] = floor(x['timeToStation']/60)
            data['secs'] = x['timeToStation'] - (data['mins'] * 60)
            data['destination'] = x['destinationName']
            data['route'] = x['lineId']
            data['name'] = x['stationName']
            if only == None:
                buses.append(data)
            else:
                if data['route'] == only:
                    buses.append(data)
    
    buses.sort(key=lambda s: (s['mins']*60) + s['secs'])
    
    return buses
def getOverground(naptan):
    
    recv = requests.get("https://api.tfl.gov.uk/Line/london-overground/Arrivals/" + naptan).json()
    trains = []
    for x in recv:
        
        if x['direction'] == overground_direction:
            print(x)
            data = {}
            data['mins'] = floor(x['timeToStation']/60)
            data['secs'] = x['timeToStation'] - (data['mins'] * 60)
            data['destination'] = x['destinationName']
            data['name'] = x['stationName']
            trains.append(data)
            
            
    trains.sort(key=lambda s: (s['mins']*60) + s['secs'])
    
    return trains
def writer():
    global active
    while True:
        try:
            color = (251,168,0)
            buses = getBus(bus_naptan, only=route)
            img = Image.new('RGB', (1000, 1200), color='black')
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("london_underground_regular-webfont.ttf", 32)
            small_font = ImageFont.truetype("london_underground_regular-webfont.ttf", 25)
            
            
            
            draw.text((200, 10),buses[0]['name'].upper() + " ARRIVALS",color,font=font)
            draw.text((0, 50),"-------------------------------------------------",color,font=font)
            spacing = 0
            for x in buses:
                spacing+=1
                text = str(spacing) + '   ' + x['route'] + ' to '  + x['destination'] + ' in ' + str(x['mins']) + ' mins ' + str(x['secs']) + ' secs'
                
                draw.text((10, spacing*45 + 50),text,color,font=font)
            end = (((spacing+2)*45) + 30)
            draw.text((0, end),"-------------------------------------------------",color,font=font)
            
            
            end += 65
            trains = getOverground(overground_naptan)
            draw.text((165, end + 10),trains[0]['name'].upper() + " ARRIVALS",color,font=font)
            draw.text((0, end + 50),"-------------------------------------------------",color,font=font)
            spacing = 0
            for x in trains:
                spacing+=1
                text = str(spacing) + '   ' + 'Overground' + ' in ' + str(x['mins']) + ' mins'
                
                draw.text((10, spacing*45 + end + 50),text,color,font=font)
            img.save('display.jpg')
            active=True
            time.sleep(interval)
        except Exception as e:
            print(e)
def reader():
    global active
    pygame.init()
    border1 = 1000
    border2 = 1200
    screen = pygame.display.set_mode((border1, border2))
    pygame.display.set_caption("TFL BUS")
    done = False
    clock = pygame.time.Clock()
    def pilImageToSurface(pilImage):
        return pygame.image.fromstring(
            pilImage.tobytes(), pilImage.size, pilImage.mode).convert()
    while not done:
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        done = True

            # Clear screen to white before drawing 
            screen.fill((0, 0, 0))
            try:
                if active:
                    img = Image.open('display.jpg')
                    active = False
                pygameSurface = pilImageToSurface(img)
                screen.blit(pygameSurface, pygameSurface.get_rect())
            except:
                print('starting')
            pygame.display.flip()
            clock.tick(60)
if __name__ == '__main__':
    w = Thread(target = writer).start()
    r = Thread(target = reader).start()
    
    