import psycopg2
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.cbook as cbook
import pandas as pd
import os
import clc_png


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

def main():

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

        # int(a.strftime('%Y%m%d'))

        if len(alert_date)!=0:
            graph_it(alert_date,alert_time,id,std_x)



def graph_it(x,y,segment,std):

    # Calculate the simple average of the data
    #mean_ = [np.std(y)] * len(y)
    min_ = [np.min(y)] * len(y)
    max_ = [np.max(y)] * len(y)

    fig, ax = plt.subplots(figsize=(25, 10))

    # Plot the data
    data_line = ax.plot(x, y, label='Second', marker='o')

    # Plot the average line
    ax.annotate('default line', xy=(5, 5), xytext=(5, 5),
                arrowprops={'arrowstyle': '-'}, va='center')
    min_line = ax.plot(x, min_, label='Minimum', linestyle='--',c='green')
    max_line = ax.plot(x, max_, label='Maximum', linestyle='--',c='red')

    plt.xlabel("Observation Time")
    plt.xticks(rotation='90')
    plt.ylabel("Travel Time (ms)")
    # Make a legend
    legend = ax.legend(loc='upper right')
    fig.figsize = (40, 40)
    plt.title('Segment Id:%s Values Higher Than AVG: %s ms'%(segment,std))
    for xs, ys in zip(x, y):
        label = "{}".format(ys)

        # this method is called for each point
        plt.annotate(label,  # this is the text
                     (xs, ys),  # this is the point to label
                     textcoords="offset points",  # how to position the text
                     xytext=(0,10),  # distance from text to points (x,y)
                     ha='center')  # horizontal alignment can be left, right or center

    if not os.path.isfile('%s.png'):

        plt.savefig('%s.png'%(segment))
    plt.show()





main()