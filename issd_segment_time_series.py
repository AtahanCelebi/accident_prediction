import psycopg2
import matplotlib.pyplot as plt


try:
    conn = psycopg2.connect(database="issd",
                                    user="postgres",
                                    password="12345Aa",
                                    host="127.0.0.1",
                                    port="5432")

    print("Successfully Connected")
except:
    print("Connection failed")

# Define a cursor to work with
cur = conn.cursor()

segment_id = 5702618

print(""" SELECT *
                FROM day_July_1
                WHERE segment_id = '{}' """.format(segment_id))

cur.execute(""" SELECT *
                FROM day_July_1
                WHERE segment_id = '{}' 
                order by discovery_time asc""".format(segment_id))

# print journey times from msec -> sec
rows = cur.fetchall()
journey_times = []

for row in rows:
    #print(row[2]/100)
    journey_times.append(row[2]/100)


plt.plot(journey_times)
plt.ylabel('Journey Time (sec)')
plt.xlabel('Observation Time')
plt.title(str(segment_id))
plt.show()

# Close the cursor and the DB connection
cur.close()
conn.close()
