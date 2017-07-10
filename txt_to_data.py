import csv, os, re
import pandas as pd

cd = os.getcwd()
text_files = os.path.join(cd,'txt/')

def extract_txt(fname):
    with open(text_files + fname,'r') as f:
        lines = f.read().splitlines()
        lines = [l for l in lines if l is not '']
        if len(lines)>1:
            park = lines[0].split(' - ')[0]
            idx = [lines.index(j) for j in lines if park in j]
            slicers = create_splits(idx)

            #Every Race in File
            races = [lines[x] for x in slicers]
            for race in races:
                extract_race_data(race)

def extract_race_data(race):
    last_raced_header = [race.index(x) for x in race if 'Last Raced' in x]
    if len(last_raced_header)>0:
        lrc_idx = last_raced_header[0]+1
        num_horses = 0
        for x in race[lrc_idx:]:
            if RepresentsInt(x[0]) or '---' in x:
                num_horses+=1
            else:
                n = num_horses
                num_horses=0
                break
        break_out_info(race,n)

def break_out_info(race,n):
    previous_races = breakout_last_races(race,n)
    horse_names = breakout_horse_names(race,n)
    print (race)

def breakout_last_races(race, n):
    lr_dict = {'Last Raced':race.index(x) for x in race if x in 'Last Raced'}
    start = (lr_dict['Last Raced'])+1
    end = start+n
    return race[slice(start,end)]

def breakout_horse_names(race, n):
    lr_dict = {'x':race.index(x) for x in race if x in 'Pgm Horse Name (Jockey)'}
    start = (lr_dict['x'])+1
    end = start+(n*2)
    pend = race[slice(start,end)]
    tmp = [x for x in pend if not any(word in x for word in ['Start','Past Performance Running Line Preview','Str'])]
    tmp =[x for x in tmp if not (RepresentsInt(x[0]) and len(x)>2)]
    return tmp

def create_splits(idx):
    #Zipper to add length
    splits = [idx[i:i + 2] for i in range(0, len(idx),1)]
    splits[-1].append(0)
    slicers = [slice(a[0],int(a[1])-1) for a in splits]
    return slicers

def RepresentsInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

if __name__=='__main__':
    for fn in os.listdir(text_files):
        extract_txt(fn)
