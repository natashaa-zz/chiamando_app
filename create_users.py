import csv
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'rssb.settings'

from django.contrib.auth.models import User

from sots.models import SOTSCallRecord

file_name = '/home/sotsadmin/Documents/users.csv'

print file_name
reader = csv.reader(open(file_name,"rb"))

for row in reader:
    user = User(first_name=row[0], email='%s@test.com' % row[0], is_active=True, username=row[0])
    user.set_password('%s123' % row[0])
    print "user %s added" % row[0]
    user.save()



