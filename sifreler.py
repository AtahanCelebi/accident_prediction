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
    cur = conn.cursor()
    cur.execute("""select *
    from dynamic_data3
    where segmentid='%s' and travel_time>(select avg(travel_time)*5
                                from dynamic_data3
                                ) order by time asc""" % (segment))
    rows = cur.fetchall()

    # Extract the column names
    anormal_obstime = []
    anormal_traveltime = []
    car_count = []

    for row in rows:
        anormal_obstime.append(row[0])
        anormal_traveltime.append(row[1])
        car_count.append(row[2])

    print("-------------------------------")
    print(anormal_obstime)

    print("values:",n_segments)





