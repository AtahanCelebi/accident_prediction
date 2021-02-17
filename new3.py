


liste1=['2020-07-01 07:23:00','2020-07-01 07:28:00','2020-07-01 07:33:00']

from datetime import datetime
fmt = '%Y-%m-%d %H:%M:%S'

new= list()
for i in liste1:
    d1 = datetime.strptime('2020-07-01 07:23:00', fmt)
    new.append('%s%s%s %s:%s:%s'%(d1.year,d1.month,d1.day,d1.hour,d1.minute,d1.second))

#y = [(i.split(':')[0]) for i in x]


x = ['%s:%s:%s'%(datetime.strptime(i,fmt).strftime("%H"),datetime.strptime(i,fmt).minute,datetime.strptime(i,fmt).strftime("%S"))  for i in liste1]
print(x)
dt = datetime.strptime('2020-07-01 07:23:00', fmt)
print(dt.strftime("%H"))