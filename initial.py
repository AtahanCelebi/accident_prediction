import psycopg2
import numpy as np
import csv



try:
    conn = psycopg2.connect(database="btr",
                            user="postgres",
                            password="de7a7838",
                            host="127.0.0.1",
                            port="5432")

    print("Successfully Connected")
except:
    print("Connection failed")



def get_all_segments():
    cur = conn.cursor()
    cur.execute(""" SELECT DISTINCT segmentid
                    FROM combination_table""")
    rows =  cur.fetchall()

    # Extract the column names
    all_segments = []
    for row in  rows:
        all_segments.append(row[0])


    return all_segments

def find_anomaly():
    segmentDict = {}
    cur = conn.cursor()
    all_segments= get_all_segments()
    count = 0
    for id in all_segments:

        print("SEGMENT:",id)
        cur.execute(""" SELECT  *
                                        FROM combination_table
                                        WHERE segmentid='{}' 
                                        order by time ASC""".format(id))

                    # print journey times from msec -> sec
        rows = cur.fetchall()
        real_time = list()
        travel_time = list()
        for row in rows:
            real_time.append(row[1])
            travel_time.append(row[2])

        std = np.average(travel_time)
        std_x = std*10
        print("NORMAL:",std)
        print("STD X5:",std_x)
        alert_time = list()
        alert_date = list()
        segment2 = list()

        for i in range(len(travel_time)):
            if int(travel_time[i]) >= int(std_x):
                alert_time.append(travel_time[i])
                alert_date.append(real_time[i])

        if not len(alert_date) ==0:
            segmentDict[int(id)] = []
            segmentDict[int(id)].append(alert_date)


    return segmentDict

anomaly_dict=find_anomaly()


with open('dict22.csv', 'w') as csv_file:
    writer = csv.writer(csv_file)
    for key, value in anomaly_dict.items():
       writer.writerow([key, value])

