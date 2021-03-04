import cv2
import json
import sys
import urlfetch

def get_drive_time(o_lat,o_long,d_lat,d_long):
    
    url = """https://api.tomtom.com/routing/1/calculateRoute/{},{}:{},{}/json?key=mHywp1xqUaq62ROfTAuCRKtxjTYA0Zak&routeType=shortest""".format(o_lat,o_long,d_lat,d_long)
    #url = "https://api.tomtom.com/traffic/map/4/tile/flow/{style}/{zoom}/{x}/{y}.{mimeType}?key=mHywp1xqUaq62ROfTAuCRKtxjTYA0Zak".format(style='absolute',zoom=12,x=1207,y=1539,mimeType='.png')
    #url="https://api.tomtom.com/map/1/wms/?request=GetMap&srs=EPSG%3A4326&bbox=-0.489%2C51.28%2C0.236%2C51.686&width=512&height=512&format=image%2Fjpeg&layers=basic&styles=&service=WMS&version=1.1.1&key=mHywp1xqUaq62ROfTAuCRKtxjTYA0Zak"
    response = urlfetch.get(url)
    try:
        
        response_json = json.loads(response.content)
        distance = response_json['routes'][0]['summary']['lengthInMeters'] #in meters
        drivetime = response_json['routes'][0]['summary']['travelTimeInSeconds'] 
    except:
        print('ERROR: in get_drive_time')
        return 0

    return [distance/1000,drivetime]

j = get_drive_time(12.935716,77.615134,12.935411,77.536093)
print(j)
def getpoints(o_lat,o_long,d_lat,d_long):
    url = "https://api.tomtom.com/routing/1/calculateRoute/{},{}:{},{}/json?key=mHywp1xqUaq62ROfTAuCRKtxjTYA0Zak".format(o_lat,o_long,d_lat,d_long)
    response = urlfetch.get(url)
    latitude=[]
    longitude=[]
    try:
        response_json = json.loads(response.content)
        points = response_json['routes'][0]['legs'][0]['points']
        for i in points:
            
            if len(i)==2:
                latitude.append(i['latitude'])
                longitude.append(i['longitude'])
            else:
                print(i)
        return [{'latpoints':latitude,'longpoints':longitude,'numofpoints':len(latitude)}]
    except:
        print('Error in getting the points')
            

def get_latlong(obname,oaname,dbname,daname):
    li = [obname,oaname,dbname,daname]
    for i in range(0,len(li)):
        li[i]=li[i].replace(' ','%20')
        li[i] = li[i].replace('.','')
    urlo="https://nominatim.openstreetmap.org/search/{}%20{}%20Bangalore?format=json&addressdetails=1&limit=1".format(li[0],li[1])
    responseo = urlfetch.get(urlo)
    urld="https://nominatim.openstreetmap.org/search/{}%20{}%20Bangalore?format=json&addressdetails=1&limit=1".format(li[2],li[3])
    responsed = urlfetch.get(urld)
    print(responseo.content)
    try:
        o_json = json.loads(responseo.content)
        d_json = json.loads(responsed.content)
        lat_o = float(o_json[0]['lat'])
        lon_o = float(o_json[0]['lon'])
        lat_d = float(d_json[0]['lat'])
        lon_d = float(d_json[0]['lon'])
        return [[lat_o,lon_o],[lat_d,lon_d]]
    except:
        print("Bt in lat long function")

def get_reverse_geo(lat,lon):
    url="https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat={}&lon={}".format(lat,lon)
    response = urlfetch.get(url)
    
    try:
        r_json = json.loads(response.content)
        roadname = r_json['display_name']
        
        return roadname
    except:
        print("Error in reverse geo code")

