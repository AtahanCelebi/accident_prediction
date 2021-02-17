from csv import reader
from datetime import datetime
import psycopg2
import numpy as np
from AnormalSegments3 import first_step
def csv_fixer():
    x = datetime.now().second
    time_dict = dict()
    with open('segdictAllStatic.csv','r') as read_obj:
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
#anormal_dict= {'1591326': [['02:28:00', '02:54:00']]}
#anormal_dict={'645872': [['09:23:00', '09:48:00'], ['14:53:00', '15:18:00'], ['16:13:00', '16:38:00'], ['17:08:00', '17:33:00']]}
#anormal_dict={'646951': [['02:48:00', '03:03:00'], ['06:53:00']]}
#anormal_dict={'656024': [['18:33:00', '18:58:00']]}
#anormal_dict={'377420': [['01:18:00', '01:43:00']]}
#anormal_dict={'3591463': [['01:23:00', '01:48:00']]}
#anormal_dict={'647921': [['01:33:00', '01:58:00']]}
#anormal_dict={'2432002': [['01:48:00', '02:13:00'], ['06:08:00', '06:13:00'], ['07:38:00'], ['21:43:00', '21:53:00']],}
#anormal_dict={'1576665': [['02:03:00', '02:28:00'], ['22:28:00', '22:38:00']]}
#anormal_dict={'645872': [['09:23:00', '09:48:00'], ['14:53:00', '15:18:00'],
#   ['16:13:00', '16:38:00'], ['17:08:00', '17:33:00']],
              #'377420': [['01:18:00', '01:43:00']], '3591463': [['01:23:00', '01:48:00']],
              #'647921': [['01:33:00', '01:58:00']]}
#anormal_dict={'645872': [['09:23:00', '09:48:00'], ['14:53:00', '15:18:00'],['16:13:00', '16:38:00'], ['17:08:00', '17:33:00']]}
neighbours_dict = dict()
anormal_dict = first_step
print("NEİGH FİNDER")
print(anormal_dict)
c=""
for key in anormal_dict.keys():
    neighbours_dict[key]=list()
    for i,j in intersection_dict.items():
        neighbours = list()
        if key==i and i not in neighbours:
            if len(j)>1:
                neighbours=[n for n in j]
                neighbours_dict[key].append(neighbours)
            else:
                neighbours.append(j[0])
                neighbours_dict[key].append(j[0])
        if key in j and c not in neighbours_dict[key]:
            findex= j.index(key)-1
            if findex== -1:
                neighbours.append(i)
                neighbours_dict[key].append(i)

            else:
                c = j[findex]
                neighbours.append(c)
                neighbours_dict[key].append(c)

print(neighbours_dict)

try:
    conn = psycopg2.connect(database="btr",
                            user="postgres",
                            password="de7a7838",
                            host="127.0.0.1",
                            port="5432")

    print("Successfully Connected")
except:
    print("Connection failed")


for segment,n_segments in neighbours_dict.items():
    take_it =list()
    print("*******************///////*****************")
    print("seg:",segment,"value",n_segments)
    for i in n_segments:
        if type(i)==list:
            for n in i:
                take_it.append(n)
        else:
            take_it.append(i)
    print("take_it:",take_it)

    for new_seg in take_it:
        cur = conn.cursor()
        cur.execute("""select *
            from dynamic_data3
            where segmentid='%s' and travel_time>(select avg(travel_time)*5
                                        from dynamic_data3
                                        ) order by time asc""" % (new_seg))
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

                if minutes >= 2 and minutes <= 5:
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

        print("shaped:",shaped_timevalues)
        for n_key2, n_value2 in anormal_dict.items():
            for n_key3, n_value3 in shaped_timevalues.items():
                if n_value3 == n_value2:
                    print("MAİNSEG:",n_key3,"THE RESULT:",n_key3,n_value2)





