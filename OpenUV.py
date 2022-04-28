import requests
import numpy as np
import matplotlib.pyplot as plt
import datetime
import time
import re


def check_time(timer):
    #2018-01-20T13:25:40.562Z
    time_check_1=re.match(r'\d{4}\-\d{2}\-\d{2}T(\d\d\:){2}\d\d\.\d*Z', timer)
    if(time_check_1==None):
        return False
    if(time_check_1.group(0)==timer):
        return True

class openUV_bot:
    API_key=open("openWetherKey.txt","r").readline()
    error_message='???Error_'
    headers = {
        'x-access-token': "86a4eddf69f84c5f49667e2f6edd32f6",
        'x-rapidapi-host': "aershov-openuv-global-real-time-uv-index-v1.p.rapidapi.com",
        'x-rapidapi-key': "6e3c601c87msh9d822b1d7ff450bp132839jsn98a739411640"
        }
    url = "https://aershov-openuv-global-real-time-uv-index-v1.p.rapidapi.com/api/v1/uv"
    
    def get_coordinates(self,s_city):
        API_key=open("openWetherKey.txt","r").readline()
        answer=requests.get("http://api.openweathermap.org/data/2.5/find",params={'q': s_city, 'type': 'like', 'units': 'metric', 'APPID': API_key})
        if(str(answer)=='<Response [200]>'):
            data=answer.json()
            if(len(data["list"])<1):
                return("???Error_city_name")
            coords=data["list"][0]['coord']
            return([coords['lat'],coords['lon']])
        return ('???Error_coordinates')
    
    def get_UV(self,coords,timer):
        if(isinstance(coords,str) and coords.startswith('???Error_')):
            return(coords)
        headers = {
            'x-access-token': "86a4eddf69f84c5f49667e2f6edd32f6",
            'x-rapidapi-host': "aershov-openuv-global-real-time-uv-index-v1.p.rapidapi.com",
            'x-rapidapi-key': "6e3c601c87msh9d822b1d7ff450bp132839jsn98a739411640"
            }
        url = "https://aershov-openuv-global-real-time-uv-index-v1.p.rapidapi.com/api/v1/uv"        
        lat=""
        lng=""
        if(len(coords)==2):
            lat=coords[0]
            lng=coords[1]
        if(len(coords)==4):
            lat="latitude, from "+str(coords[0])+" to "+str(coords[2])
            lng="longitude, from "+str(coords[1])+" to "+str(coords[3])
        if(timer=='now'):
            time=str(datetime.datetime.now())
            day, hours=time.split()
            time=day+"T"+hours+"Z"
        querystring={"lat":lat,"lng":lng,"alt":"0","dt":time}
        response = requests.request("GET", url, headers=headers, params=querystring) 
        response=response.json()
        print(response)
        if('result' in response.keys()):
            if('sun_info' in response['result']):
                if('sun_position' in response['result']['sun_info']):
                    return(response['result']['sun_info']['sun_position'])
        return('???Error_get_UV')
        
    def azimuth_plt(self,coords,time_begin,time_end,period):
        try:
            if(check_time(time_begin)!=True and time_begin!="now"):
                raise Exception('time_begin must be in format 2018-01-20T13:25:40.562Z')
            headers = {
                'x-access-token': "86a4eddf69f84c5f49667e2f6edd32f6",
                'x-rapidapi-host': "aershov-openuv-global-real-time-uv-index-v1.p.rapidapi.com",
                'x-rapidapi-key': "6e3c601c87msh9d822b1d7ff450bp132839jsn98a739411640"
                }
            url = "https://aershov-openuv-global-real-time-uv-index-v1.p.rapidapi.com/api/v1/uv"        
            lat=""
            lng=""
            if(len(coords)==2):
                lat=coords[0]
                lng=coords[1]
            if(len(coords)==4):
                lat="latitude, from "+str(coords[0])+" to "+str(coords[2])
                lng="longitude, from "+str(coords[1])+" to "+str(coords[3])
                
            start_time=time.time()
            counter=0
            times=[i for i in range(time_end)]
            azimuths=[]
            while(counter<time_end):
                if(time_begin=='now'):
                    timec=str(datetime.datetime.now())
                    day, hours=timec.split()
                    timec=day+"T"+hours+"Z"
                else:
                    while(time.time<time_begin):
                        pass
                    timec=''
                querystring={"lat":lat,"lng":lng,"alt":"0","dt":timec}
                response = requests.request("GET", url, headers=headers, params=querystring) 
                response=response.json()
                #print(response)
                try:
                    azimuths.append(response['result']['sun_info']['sun_position']["azimuth"])
                except:
                    azimuths.append(-1)
                while(time.time()-start_time<period):
                    pass    
                start_time=time.time()
                counter+=1
                print(counter)
            plt.plot(times, azimuths)
            plt.savefig('viz.png')
            return('viz.png')
        except:
            return('error.png')
        
    def altitude_plt(self, coords,time_begin,time_end,period):
        if(check_time(time_begin)!=True and time_begin!="now"):
            raise Exception('time_begin must be in format 2018-01-20T13:25:40.562Z')
        headers = {
            'x-access-token': "86a4eddf69f84c5f49667e2f6edd32f6",
            'x-rapidapi-host': "aershov-openuv-global-real-time-uv-index-v1.p.rapidapi.com",
            'x-rapidapi-key': "6e3c601c87msh9d822b1d7ff450bp132839jsn98a739411640"
            }
        url = "https://aershov-openuv-global-real-time-uv-index-v1.p.rapidapi.com/api/v1/uv"        
        lat=""
        lng=""
        if(len(coords)==2):
            lat=coords[0]
            lng=coords[1]
        if(len(coords)==4):
            lat="latitude, from "+str(coords[0])+" to "+str(coords[2])
            lng="longitude, from "+str(coords[1])+" to "+str(coords[3])
            
        start_time=time.time()
        counter=0
        times=[i for i in range(time_end)]
        altitudes=[]
        while(counter<time_end):
            if(time_begin=='now'):
                timec=str(datetime.datetime.now())
                day, hours=timec.split()
                timec=day+"T"+hours+"Z"
            else:
                while(time.time<time_begin):
                    pass
                timec=''
            querystring={"lat":lat,"lng":lng,"alt":"0","dt":timec}
            response = requests.request("GET", url, headers=headers, params=querystring) 
            response=response.json()
            #print(response)
            altitudes.append(response['result']['sun_info']['sun_position']["altitude"])
            while(time.time()-start_time<period):
                pass    
            start_time=time.time()
            counter+=1
            print(counter)
        return([times,altitudes])
         
if __name__=="__main__":
    bot=openUV_bot()
    city="Irkutsk"
    #city=input()
    #print(check_time('2018-01-20T13:25:40.562Z'))
    coord=bot.get_coordinates(city)
    bot.get_UV(coord,"now")
    #bot.azimuth_plt(coord,"now", 10, 1)
    #times, altitudes=bot.altitude_plt(coord,"now",10,1)
    #plt.plot(times,altitudes)
    #plt.savefig('viz.png')
    
#NodeRed yED