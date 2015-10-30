import csv
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'rssb.settings'



from sots.models import SOTSCallRecord

file_name = '/home/sotsadmin/Documents/records.csv'

print file_name

writer = csv.writer(open(file_name,"w"))

records = SOTSCallRecord.objects.all()

model = records.model
    
headers = []
for field in model._meta.fields:
    headers.append(field.name)

writer.writerow(headers)
    
for obj in records:
    row = []
    for field in headers:
        val = getattr(obj, field)
        if callable(val):
            val = val()
        if type(val) == unicode:
            val = val.encode("utf-8")
        row.append(val)
    writer.writerow(row)



