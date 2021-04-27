"""
Created: 27/04/2021
@author: AtahanCelebi
"""

import psycopg2
import csv
from datetime import datetime
from excessive_time_limit import excessive_time_limit
def find_linked_time(avg=2,min=2,max=10):

    conn = psycopg2.connect(database="issd",
                                user="postgres",
                                password="issd",
                                host="127.0.0.1",
                                port="5432")



    cur = conn.cursor()
    ###This query finds anormal-segments which are x10 times higher than the average
    cur.execute(""" select c1.segmentid, c1.time,c1.travel_time
    from istanbul_veri4 c1
    where c1."roadClass"=1 and c1.travel_time > (select avg(c2.travel_time)*%s
                            from istanbul_veri4 c2)
                            order by c1.time asc"""%(avg))
    rows = cur.fetchall()

    # Extract the column names
    anormal_segments = []
    anormal_time = []

    for row in rows:
        anormal_segments.append(row[0])
        anormal_time.append(row[1])
    #print(avg,"kat yüksek averaj olan dictionary:\n",anormal_time)
    # We are currently working on one day, so we reshaped the observation time

    fmt = '%Y-%m-%d %H:%M:%S'
    shaped_time = x = ['%s-%s-%s %s:%s:%s' % (datetime.strptime(str(i), fmt).strftime("%Y"),datetime.strptime(str(i), fmt).strftime("%m"),datetime.strptime(str(i), fmt).strftime("%d"),datetime.strptime(str(i), fmt).strftime("%H"), datetime.strptime(str(i), fmt).strftime("%M"),
                                     datetime.strptime(str(i), fmt).strftime("%S")) for i in anormal_time]

    dct = dict() #id and time variable are zipped
    for i, j in zip(anormal_segments, shaped_time):
        dct.setdefault(str(i), []).append(str(j))
    print(dct)
    #print("id ve segment olarak düzenlenmiş hali\n",dct)


    shaped_timevalues = dict()
    fmt = '%Y-%m-%d %H:%M:%S'

    for i, j in  dct.items():
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

    #print(shaped_timevalues)

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

    csv_columns = ['SegmentsId', 'ObservationTime']
    with open("AnormalTimeAVG.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for i, j in shaped_timevalues.items():
            # print('SEGMENT:',i,'TIMES:',j)
            csvfile.write('%s,%s\n' % (i, j))
    print("İlgili zaman aralıkları eşlenmiş SON hali\n",shaped_timevalues)
    return shaped_timevalues #Final dictionary returns if they are linked


first_step=(excessive_time_limit(find_linked_time(avg=15),limit=10))















