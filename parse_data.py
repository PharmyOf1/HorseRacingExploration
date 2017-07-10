import requests, os, time, magic
import subprocess
from random import choice
from datetime import datetime, timedelta

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

cur_dur = os.path.join(os.getcwd(),'pdfs/')

def extract_data(fname,data):
    txt_dur = os.path.join(os.getcwd(),'txt/')
    outfile = txt_dur + '{track}{year}{month}{day}.txt'.format(**data)
    pdf_text = subprocess.run(['pdf2txt.py',fname, '-o',outfile])

def download_pdf(url,data):
    fname = '/home/una0464/projects/horseracing/pdfs/horsedata-{track}{year}{month}{day}.pdf'.format(**data)
    txt_dur = os.path.join(os.getcwd(),'txt/')
    outfile = txt_dur + '{track}{year}{month}{day}.txt'.format(**data)
    if not os.path.isfile(outfile):
        r = requests.get(url,headers={'User-Agent':'HORSE'})
        if len(r.content)>0:
            with open(fname, 'wb') as f:
                f.write(r.content)

            pdf_check = magic.from_file(fname).split(' ')[0]
            if pdf_check == 'PDF':
                decrypt_pdf(fname,data)
            else:
                print ('Probably banned')
            os.remove(fname)
            time.sleep(choice([60]))
    else:
        pass


def decrypt_pdf(fname,data):
    new_file = cur_dur + '{track}{year}{month}{day}-de.pdf'.format(**data)
    print ('Got {track}-{month}-{day}-{year}.pdf'.format(**data))
    subprocess.run(['qpdf','--decrypt',fname,new_file])
    extract_data(new_file,data)
    print ('Decrypted')
    os.remove(new_file)

def get_all_txt(parks, day, month, year):
    data = {'track': track,'month':month,'day':day,'year':year}
    url = 'http://www.equibase.com/premium/eqbPDFChartPlus.cfm?RACE=A&BorP=P&TID={track}&CTRY=USA&DT={month}/{day}/{year}&DAY=D&STYLE=EQB'
    url = url.format(**data)
    try:
        download_pdf(url,data)
    except:
        pass


if __name__ == '__main__':
    parks =[
    'ARP', 'AP','ASD','BEL','BTP','CBY','CPW','CD','DEL','DED','EMD','EVD','FMT',
    'FL','GG','GRP','GP','HP','CT','IND','LBT','LRL','LBG','LS','LAD','MD','MTH',
    'NP','PEN','PRM','RET','RUI','SA','SRP','TDN','WO']

    d = datetime.today()
    for track in parks:
        for x in range(1540):
            d = d - timedelta(days=1)
            day = '{:02d}'.format(d.day)
            month = '{:02d}'.format(d.month)
            year = '{:02d}'.format(d.year)

            get_all_txt(parks,day, month, year)
