from datetime import datetime
import csv
def excessive_time_limit(reshaped_time,limit):
    #This function finds the excessive time SegmentID
    #and their time interval
    fmt = '%H:%M:%S'
    newdct = dict()
    for i, j in reshaped_time.items():
        newlist = list()
        sequence = [j[0]]
        for n in range(0,len(j)):

            if len(j[n])==2:

                time1 = datetime.strptime(j[n][0], fmt)
                time2 = datetime.strptime(j[n][-1], fmt)
                minutes = (time2 - time1).total_seconds() / 60  # how many minutes in difference

                if minutes >= limit : # for 1st July max 26 min
                    #newlist.append([i,j[n]])
                    newlist.append(j[n])
                    newdct[i] = newlist
    """
    csv_columns = ['SegmentsId', 'ObservationTime']
    with open("AnormalTimeInterval.csv", 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for i, j in newdct.items():
            # print('SEGMENT:',i,'TIMES:',j)
            csvfile.write('%s,%s\n' % (i, j))"""
    print(limit,"dakika limit değerine göre ayarlanmış dictionary\n",newdct)
    return newdct

