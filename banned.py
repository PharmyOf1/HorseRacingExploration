import requests, os, time, magic
import subprocess
from random import choice
from datetime import datetime, timedelta
from PIL import Image
import requests
from io import BytesIO

d = datetime.today()
d = d - timedelta(days=1)
day = '{:02d}'.format(d.day)
month = '{:02d}'.format(d.month)
year = '{:02d}'.format(d.year)
track = 'ARP'

data = {'track': track,'month':month,'day':day,'year':year}
url = 'http://www.equibase.com/premium/eqbPDFChartPlus.cfm?RACE=A&BorP=P&TID={track}&CTRY=USA&DT={month}/{day}/{year}&DAY=D&STYLE=EQB'
url = url.format(**data)
r = requests.get(url,headers={'User-Agent':'HORSE'})

if (r.status_code) == 691:
    print (r.text)
    captcha_img = r.text
    captcha_txt = 'the_answer'
payload = {'captcha':r"%26%3C532%5F%28FH%0A",
            'ks':"2",
            'ke':"12",
            'rt':"0",
            'request':"/premium/eqbPDFChartPlus.cfm?…T=06/18/2017&DAY=D&STYLE=EQB",
            'resource':"CHPLU",
            'site':"EQB",
            'userText': captcha_txt}
