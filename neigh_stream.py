from csv import reader
from datetime import datetime
import psycopg2
import numpy as np
from AnormalSegments3 import first_step
anormal_dict = first_step
segment_check= list()
def csv_fixer():
    x = datetime.now().second
    time_dict = dict()
    with open('segdictAllStatic.csv','r') as read_obj:# Thanks to Mete, segment neighbours csv
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
    key_neighbours = dict()
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
            findex = j.index(key) - 1
            if findex == -1:
                neighbours.append(i)
                key_neighbours[key].append(i)

            else:
                c = j[findex]
                neighbours.append(c)
                key_neighbours[key].append(c)
    return key_neighbours

try:
    conn = psycopg2.connect(database="btr",
                            user="postgres",
                            password="de7a7838",
                            host="127.0.0.1",
                            port="5432")

    #print("Successfully Connected")
except:
    #print("Connection failed")
    pass

def goster(new_seg,anormal_obstime,anormal_segments,min=2,max=5):
    print("segment:", new_seg, "-------------------------------")
    print(anormal_obstime)
    # We are currently working on one day, so we reshaped the observation time
    fmt = '%Y-%m-%d %H:%M:%S'
    shaped_time = x = [
        '%s:%s:%s' % (datetime.strptime(i, fmt).strftime("%H"), datetime.strptime(i, fmt).strftime("%M"),
                      datetime.strptime(i, fmt).strftime("%S")) for i in anormal_obstime]

    dct = dict()
    for i, j in zip(anormal_segments, shaped_time):
        dct.setdefault(i, []).append(j)

    print(dct)

    shaped_timevalues = dict()
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

    for key in shaped_timevalues.keys():
        # print('SEGMENTID',key)
        # print('LENGTH:',len(shaped_timevalues[key]))
        c = 0
        for j in shaped_timevalues[key]:
            # print(j)
            remake = list()
            if len(j) > 2:
                remake.append(j[0])
                remake.append(j[-1])
                if remake not in shaped_timevalues[key]:
                    shaped_timevalues[key][c] = remake
            c += 1

    print("shaped:", shaped_timevalues)


def sorgu(komsular,avg=5):
    for new_seg in komsular:
        print("NEW SEG:",new_seg)
        cur = conn.cursor()
        cur.execute("""select *
                        from dynamic_data3
                        where segmentid='%s' and travel_time>(select avg(travel_time)*%s
                                                    from dynamic_data3
                                                    ) order by time asc""" % (new_seg, avg))

        rows = cur.fetchall()

        # Extract the column names
        anormal_obstime = []
        anormal_segments = []
        anormal_traveltime = []
        car_count = []

        for row in rows:
            anormal_obstime.append(row[0])
            anormal_segments.append(row[1])
            anormal_traveltime.append(row[2])
            car_count.append(row[3])
        goster(new_seg, anormal_obstime, anormal_segments)
        print(len(anormal_obstime),"veeeee",segment_check)

        while (len(anormal_obstime)>=3 and new_seg not in segment_check ):
            if new_seg not in segment_check:
                segment_check.append(new_seg)
                komsular2=find_key(new_seg)
                sorgu(komsular2[new_seg])




for i,j in anormal_dict.items():
    if i not in segment_check:
        segment_check.append(i)
        komsular = find_key(i)
        #print(i,"komşular:",komsular[i],len(komsular[i]))
        sorgu(komsular[i])
