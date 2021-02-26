from csv import reader
from datetime import datetime
import psycopg2
import numpy as np
from AnormalSegments3 import first_step

neighbours_dict = dict()
anormal_dict = first_step
print("NEİGH FİNDER")
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


def find_neighbours_if_anormal(avg,min=2,max=5):#5874021 , 5874023, 644068, 5605488, 1575603
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
        #print("take_it:",take_it)

        for new_seg in take_it: #RECURSION MUST!!!
            cur = conn.cursor()
            cur.execute("""select *
                from dynamic_data3
                where segmentid='%s' and travel_time>(select avg(travel_time)*%s
                                            from dynamic_data3
                                            ) order by time asc""" % (new_seg,avg))

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

            print("shaped:",shaped_timevalues)

find_neighbours_if_anormal(5)


