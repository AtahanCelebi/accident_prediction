"""
Created: 10/04/2021
@author: AtahanCelebi
"""

from csv import reader
from datetime import datetime
import psycopg2
import numpy as np
from datetime import datetime as dt
from AnormalSegments3 import first_step
anormal_dict = first_step
segment_check= list()
shaped_timevalues = dict()

def csv_fixer():
    x = datetime.now().second
    time_dict = dict()
    with open("C:\\Users\\Ata\\Desktop\\istanbul_neigh.csv",'r') as read_obj:# Thanks to Mete, segment neighbours csv
            csv_reader = reader(read_obj)
            header = next(csv_reader)
            # Check file as empty
            if header != None:
                # Iterate over each row after the header in the csv

                for row in csv_reader:
                    while ("" in row):
                        row.remove("")
                    if len(row)>1:
                        time_dict[row[0]]=row[1:]
                    #374614 segment is empty!!!

    #for i,j in time_dict.items():
        #print("segmetns:",i,"values:",j)
    return time_dict

intersection_dict=csv_fixer()

def find_key(key):
    key_neighbours = dict() #exp:1553031 , 1553026
    c = ""
    key_neighbours[key] = list()
    for i, j in intersection_dict.items():
        neighbours = list()
        if key == i and i not in neighbours:
            if len(j) > 1:
                for n in j:
                    key_neighbours[key].append(n)
            else:
                neighbours.append(j[0])
                key_neighbours[key].append(j[0])
        if key in j and c not in key_neighbours[key]:
            neighbours.append(i)
            key_neighbours[key].append(i)


    return key_neighbours

try:
    conn = psycopg2.connect(database="btr",
                            user="postgres",
                            password="de7a7838",
                            host="127.0.0.1",
                            port="5434")

    #print("Successfully Connected")
except:
    #print("Connection failed")
    pass

def goster(new_seg,anormal_obstime,anormal_segments,min=2,max=5):
    #print("segment:", new_seg, "-------------------------------")
    #print(anormal_obstime)
    # We are currently working on one day, so we reshaped the observation time
    fmt = '%Y-%m-%d %H:%M:%S'
    shaped_time = x = [
        '%s:%s:%s' % (datetime.strptime(i, fmt).strftime("%H"), datetime.strptime(i, fmt).strftime("%M"),
                      datetime.strptime(i, fmt).strftime("%S")) for i in anormal_obstime]

    dct = dict()
    for i, j in zip(anormal_segments, shaped_time):
        dct.setdefault(i, []).append(j)

    #print(dct)

    fmt = '%H:%M:%S'

    for i, j in dct.items():
        newlist = list()
        sequence = [j[0]]  # list with the 'linked times', with the first value already inserted
        for n in range(1, len(j)):

            time1 = datetime.strptime(j[n - 1], fmt)
            time2 = datetime.strptime(j[n], fmt)
            minutes = (time2 - time1).total_seconds() / 60  # how many minutes in difference

            if minutes >= min and minutes <= max:
                sequence.append(j[n])

            else:
                newlist.append(sequence)
                sequence = [j[n]]

        if len(sequence) > 0:
            newlist.append(sequence)
        shaped_timevalues[i] = newlist

    # print(shaped_timevalues)
    if shaped_timevalues.get(new_seg) is not None:
        c = 0
        for j in shaped_timevalues[new_seg]:
                # print(j)
            remake = list()
            if len(j) > 2:
                remake.append(j[0])
                remake.append(j[-1])
                if remake not in shaped_timevalues[new_seg]:
                    shaped_timevalues[new_seg][c] = remake
            c += 1

def sorgu(komsular,key,avg=5):
    for new_seg in komsular:
        if new_seg not in segment_check:
            cur = conn.cursor()
            cur.execute("""select *
                            from istanbul_veri
                            where segmentid='%s' and travel_time>(select avg(travel_time)*%s
                                                        from istanbul_veri
                                                        ) order by time asc""" % (new_seg, avg))

            rows = cur.fetchall()
            # Extract the column names
            anormal_obstime = []
            anormal_segments = []
            anormal_traveltime = []
            car_count = []

            for row in rows:
                anormal_obstime.append(str(row[0]))
                anormal_segments.append(row[1])
                anormal_traveltime.append(row[2])
                car_count.append(row[3])
            goster(new_seg, anormal_obstime, anormal_segments)
            if shaped_timevalues.get(new_seg) is  None:
                print("NEW SEG-----x", new_seg)
            else:
                print("NEW SEG-----", new_seg)
                print("shaped:", new_seg,":",shaped_timevalues[new_seg])
                get = time_match(anormal_dict[key], shaped_timevalues[new_seg])

                while get and new_seg not in segment_check:
                    segment_check.append(new_seg)
                    komsular2 = find_key(new_seg)
                    # print("SEGMENT LISTESI:", segment_check)
                    print("%s'in Komşuları:%s" % (new_seg, komsular2))
                    sorgu(komsular2[new_seg], key)




def time_match(main,neigh):
    print("************************main:::",main)
    print("************************neigh:::",neigh,len(neigh))

    for i in range(len(neigh)):
        for j in range(len(main)):
            for x in neigh[i]:
                for y in main:
                    start = y[0]
                    end = y[1]
                    if dt.strptime(start, "%H:%M:%S") <= dt.strptime(x, "%H:%M:%S") <= dt.strptime(end, "%H:%M:%S"):
                        print("*****EŞLEŞTİ","x:",x,"y:",y)
                        return True
    return False

for i,j in anormal_dict.items():
    if i not in segment_check:
        segment_check.append(i)
        komsular = find_key(i)
        print("--------------------------------------------------",i,"komşular:",komsular[i],len(komsular[i]),"--------------------------------------------------")
        sorgu(komsular[i],i)
