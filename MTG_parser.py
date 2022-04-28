import requests
from io import BytesIO
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import os
from PIL import Image
from io import BytesIO
from mtgsdk import Card
from mtgsdk import Set
import re
import json


#https://github.com/MagicTheGathering/mtg-sdk-python
class MTG_bot:
    
    err_msg="???Error_"
    goldfish_rate=50
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}
    last_name='Asmoranomardicadaistinaculdacar'
    commands=['!help', '!trans','!top','!gf','!exit','!img','!name','!topdeckfull','!checktop']
    
    def get_help(self):
        print("!trans <название карты/часть названия> – название карты на русском и английском")
        print("!trans _ – название последней вбитой карты на русском и английском")
        print("!top <название карты> – минимальная цена на Topdeck")
        print("!top _ – минимальная цена последней вбитой карты на Topdeck")
        print("!name <название карты> – вбить название в бота")
        print("!name _ – вывести последнюю вбитую карту")
        print("!gf <название карты> – цены с сайта goldfish по выпускам")
        print("!gf _ – цены последней вбитой карты с сайта goldfish по выпускам")
        print("!top _ – минимальная цена последней вбитой карты на Topdeck")
        print("!img <название карты> – изображение карты")
        print("!topdeckfull получить все данные с сайта topdeck")
        print("!exit - завершить работу")
        
    
    def clean_name(self,mas):
        result=mas
        i=0
        while(i<len(result)):
            if(result[i]=='' or result[i].isdigit()):
                mas.pop(i)
            else:
                if(isinstance(mas[i],str)):
                    result[i]=mas[i].replace('\r','')
                    result[i]=mas[i].replace('\n','')
                i+=1
        return(result)
        
    
    def mas_eq(self,mas1,mas2):
        if(len(mas1)!=len(mas2)):
            return False
        for i in range(len(mas1)):
            if(mas1[i]!=mas2[i]):
                return False
        return True
    
    def mas_as(self,mas1,mas2):
        if(len(mas1)!=len(mas2)):
            return False
        for i in range(len(mas1)):
            if(mas1[i] not in mas2[i]):
                return False
        return True    
    
    
    def search_mtg_ru(self,cardname):
        if(cardname.startswith('???Error_')):
            return(cardname)
        cardname=cardname.lower()
        splitted_name=cardname.split(' ')
        mtgruURL='http://www.mtg.ru/cards/search.phtml?Title='+cardname
        full_page = requests.get(mtgruURL, headers=self.headers)
        soup = BeautifulSoup(full_page.content, 'html.parser')
        message=soup.findAll('span', attrs={'id':'B'})
        if ('не найдено' in str(message[0])):
            return("???Error_translate")
        else:
            start_time=time.time()
            resultstring=None
            firstchoose=None
            i=2
            while(True):
                names = soup.findAll('h2')
                if(len(names)<2):
                    break
                if(firstchoose==None):
                    firstchoose=names[1].text
                for name in names[1:]:
                    if(len(name.text.split('//'))>1):
                        first_name,second_name=name.text.split('//')
                        first_name=first_name.lower()
                        second_name=second_name.lower()
                        splitted_first=first_name.split(' ')
                        splitted_second=second_name.split(' ')
                        splitted_first=self.clean_name(splitted_first)
                        splitted_second=self.clean_name(splitted_second)
                        #print(splitted_first,' ',splitted_second,' ',splitted_name)
                        if(self.mas_eq(splitted_first, splitted_name)):
                            resultstring=name.text
                        if(self.mas_eq(splitted_second, splitted_name)):
                            resultstring=name.text
                        if(self.mas_as(splitted_name, splitted_first) and resultstring==None):
                            resultstring=name.text
                        if(self.mas_as(splitted_name, splitted_second) and resultstring==None):
                            resultstring=name.text
                    else:
                        first_name=name.text
                        first_name=first_name.lower()
                        splitted_first=first_name.split(' ')
                        splitted_first=self.clean_name(splitted_first)
                        #print(splitted_first,' ',splitted_name)
                        if(self.mas_eq(splitted_first, splitted_name)):
                            resultstring=name.text
                        if(self.mas_as(splitted_name, splitted_first) and resultstring==None):
                            resultstring=name.text
                mtgruURL='http://www.mtg.ru/cards/search.phtml?Title='+cardname+'&page='+str(i)
                i+=1
                full_page = requests.get(mtgruURL, headers=self.headers)
                soup = BeautifulSoup(full_page.content, 'html.parser')
                if(time.time()-start_time>10):
                    return ('???Error_translate')
            if(resultstring==None):
                resultstring=firstchoose 
            self.last_name=resultstring.split('/')[0].strip()
            while(self.last_name[len(self.last_name)-1].isdigit() or self.last_name[len(self.last_name)-1]==' '):
                self.last_name=self.last_name[:-1]
            resultstring=resultstring.split(' // ')[0]
            resultstring=resultstring.lstrip()
            return resultstring
    
    
    def get_price_topdeck(self,name):
        if(name.startswith('???Error_')):
            return(name)
        if(name=='_'):
            name=self.last_name
        options=webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("--headless")
        path = os.path.abspath(os.curdir)
        path=path+"\\chromedriver.exe"
        driver=webdriver.Chrome(options=options, executable_path=path)
        TopdeckURL='https://topdeck.ru/apps/toptrade/singles/search?q='
        name='+'.join(name.split())
        TopdeckURL=TopdeckURL+name
        driver.get(TopdeckURL)
        #driver.find_element_by_id('q').send_keys(name)
        #driver.find_elements_by_tag_name('button')[1].click()
        #time.sleep(1)
        cost=-1
        traders=driver.find_elements_by_tag_name('a')
        if(len(traders)<20):
            return("???Error_topdeck")
        for i in range(20,len(traders),2):
            cost=driver.find_elements_by_tag_name('td')[6+5*int((i-20)/2)].text
            break
        #print(f'Цена на TopDeck от {cost} р.')
        return(cost)
    
    def get_stat_topdeck(self, name, mode):
        full_info=self.get_full_info_topdeck(name)
        if(isinstance(full_info,str) and full_info.startswith('???Error_')):
            return(full_info)
        mas=[]
        print(mode,' ',mode=="plot")
        for key in full_info.keys():
            for key1 in full_info[key].keys():
                for price in full_info[key][key1]:
                    mas.append(price)
        if(mode=="list"):
            return(mas)
        if(mode=="plot"):
            mas=sorted(mas)
            values={}
            for i in range(len(mas)):
                if(mas[i] in values.keys()):
                    values[mas[i]]+=1
                else:
                    values[mas[i]]=1
            masx=[]
            masy=[]
            for key in values.keys():
                masx.append(key)
                masy.append(values[key])
            plt.bar(masx,masy)
            plt.savefig("figure_mtg.png")
            return("figure_mtg.png")
                
        return("???Error_mode")
        
        
    def get_full_info_topdeck(self,name):
        if(name=='_'):
            name=self.last_name
        options=webdriver.ChromeOptions()
        options.add_argument("--log-level=3")
        options.add_argument("--headless")
        path = os.path.abspath(os.curdir)
        path=path+"\\chromedriver.exe"
        driver=webdriver.Chrome(options=options, executable_path=path)
        TopdeckURL='https://topdeck.ru/apps/toptrade/singles/search?q='
        name='+'.join(name.split())
        TopdeckURL=TopdeckURL+name
        driver.get(TopdeckURL)
        tds=driver.find_elements_by_tag_name('td')
        result={}
        for i in range(20,len(tds),2):
            if(8+5*int((i-20)/2)<len(tds)):
                price=tds[6+5*int((i-20)/2)].text
                name=tds[7+5*int((i-20)/2)].text
                if(len(name.split())>1):
                    name=name.split()[1]
                city=tds[8+5*int((i-20)/2)].text
                if(city in result.keys()):
                    if(name in result[city].keys()):
                        result[city][name].append(price)
                    else:
                        result[city][name]=[price]
                else:
                    result[city]={name:[price]}
                #print("{p:10s}{n:20s}{c:20s}".format(p = price, n=name, c=city))
        return result
        
        
    def get_price_Goldfish(self,name):
        print(name)
        if(name.startswith('???Error_')):
            return(name)
        if(name=='_'):
            name=self.last_name
        URL='https://www.mtggoldfish.com/price/'
        cards = Card.where(name=name).all()
        visited_sets=[]
        with open("sets.json", "r") as read_file:
            data = json.load(read_file)
        for card in cards:
            #print(card.set)
            if(card.set in data and card.set not in visited_sets):
                visited_sets.append(card.set)
                sets=data[card.set].split('/')
                for seter in sets:
                    mtggoURL=URL+('+'.join(seter.split()))+'/'+('+'.join(name.split()))+'#paper'
                    full_page = requests.get(mtggoURL, headers=self.headers)
                    if(full_page.status_code==200):
                        print(seter)
                        soup = BeautifulSoup(full_page.content, 'html.parser')
                        price=soup.findAll('div', attrs={'class':'price-box-price'})
                        if(len(price)>0 and price!=None):
                            #print(price[0].text)
                            return(price[0].text)
                        else:
                            return('???Error_Goldfish')
                            
    def get_less_price_Goldfish(self,name):
        if(name.startswith('???Error_')):
            return(name)
        if(name=='_'):
            name=self.last_name
        URL='https://www.mtggoldfish.com/price/'
        cards = Card.where(name=name).all()
        visited_sets=[]
        current_price=None
        with open("sets.json", "r") as read_file:
            data = json.load(read_file)
        for card in cards:
            #print(card.set)
            if(card.set in data and card.set not in visited_sets):
                visited_sets.append(card.set)
                sets=data[card.set].split('/')
                for seter in sets:
                    mtggoURL=URL+('+'.join(seter.split()))+'/'+('+'.join(name.split()))+'#paper'
                    full_page = requests.get(mtggoURL, headers=self.headers)
                    if(full_page.status_code==200):
                        soup = BeautifulSoup(full_page.content, 'html.parser')
                        price=soup.findAll('div', attrs={'class':'price-box-price'})
                        if(len(price)>0):
                            s=price[0].text.split()
                            if(current_price==None or float(s[1])<current_price):
                                current_price=float(s[1])
        return(current_price)
    
    def find_all_normal_prices(self,name):
        normal_price=self.get_less_price_Goldfish(name)*self.goldfish_rate
        all_prices=self.get_full_info_topdeck(name)
        print('курс goldfish: ',normal_price)
        found=False
        for city in all_prices.keys():
            for name in all_prices[city].keys():
                for price in all_prices[city][name]:
                    #print(price)
                    if(int(price)<=normal_price):
                        found=True
                        print("{p:10s}{n:20s}{c:20s}".format(p = price, n=name, c=city))
        if(found==False):
            print('дешевле нет')
                    
    def get_image(self,name):
        if(name=='_'):
            name=self.last_name
        URL='https://www.mtggoldfish.com/price/'
        cards = Card.where(name=name).all()
        link=''
        with open("sets.json", "r") as read_file:
            data = json.load(read_file)
        for card in cards:
            if(card.set in data):
                seters=data[card.set].split('/')[0]
                mtggoURL=URL+('+'.join(seters.split()))+'/'+('+'.join(name.split()))+'#paper'
                #print(mtggoURL)
                full_page = requests.get(mtggoURL, headers=self.headers)
                if(full_page.status_code==200):
                    soup = BeautifulSoup(full_page.content, 'html.parser')
                    link=soup.findAll('source', attrs={'type':'image/jpg'})[0]['srcset']
                    break
        link=link.split()[0]
        r = requests.get(link, stream = True)
        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))
            img.show()

    
if __name__=='__main__':
    bot=MTG_bot()
    while(True):
        line=input()
        line=line.strip()
        if(line=='!exit'):
            break
        if(line=='!help'):
            bot.get_help()
        if(len(line.split())<2):
            continue
        command=line.split()[0]
        name=' '.join(line.split()[1:])
        if(command not in bot.commands):
            print('команда не распознана')
            continue
        if(command=='!trans'):
            result=bot.search_mtg_ru(name)
            print(result)
        if(command=='!checktop'):
            result=bot.find_all_normal_prices(name)
            print(result)
        if(command=='!top'):
            bot.get_stat_topdeck(name,"plot")
        if(command=='!topdeckfull'):
            result=bot.get_full_info_topdeck(name)
            print(result)
        if(command=='!gf'):
            bot.get_price_Goldfish(name)
            #result=bot.get_less_price_Goldfish(name)
            #print(result)
        if(command=='!img'):
            bot.get_image(name)
        if(command=='!name'):
            if(name=='_'):
                print(bot.last_name)
            else:
                bot.last_name=name
    