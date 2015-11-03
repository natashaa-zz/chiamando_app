import csv
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'rssb.settings'

from sots.models import SOTSCallRecord

file_name = '/home/sotsadmin/Documents/MasterTable.csv'

print file_name
COUNTRY_CODE = '+971'


reader = csv.DictReader(open(file_name))
headers = reader.fieldnames
#reader = csv.reader(open(file_name,"rb"))

## Delete the existing records

records = SOTSCallRecord.objects.all()
records.delete()
for row in reader:
    try:
        if int(row.get('FamilyID')):
           continue
        row_info = {
            'ssrecid': int(row.get('SSRecID')),
            'familyid': int(row.get('FamilyID')),
            'firstname': row.get('SSFName'),
            'middlename': row.get('SSMName'),
            'lastname': row.get('SSLName'),
            'emergency_contact1_name': row.get('EContactPersonlocal'),
            'emergency_contact2_name': row.get('ESContactPersonlocal'),
          
        }
        if int(row.get('Mobile')) and int(row.get('MobExt')):
            row_info.update({'mobile1': '%s%s%s' % (COUNTRY_CODE, row.get('MobExt'), row.get('Mobile'))})

        if int(row.get('Mobile1')) and int(row.get('MobExt1')):
            row_info.update({'mobile2': '%s%s%s' % (COUNTRY_CODE, row.get('MobExt1'), row.get('Mobile1'))})

        if int(row.get('ResTel')) and int(row.get('ResTelExt')):
            row_info.update({'landline': '%s%s%s' % (COUNTRY_CODE, row.get('ResTelExt'),
                                                     row.get('ResTel'))})

        if int(row.get('EContactNumber')) and int(row.get('EContactNumberExt')):
            row_info.update({'emergency_contact1': '%s%s%s' % (COUNTRY_CODE, row.get('EContactNumberExt'),
                                                               row.get('EContactNumber'))})

        if int(row.get('ESContactNumber')) and int(row.get('ESContactNumberExt')):
            row_info.update({'emergency_contact2': '%s%s%s' % (COUNTRY_CODE, row.get('ESContactNumberExt'),
                                                               row.get('ESContactNumber'))})


        call_record = SOTSCallRecord(**row_info)
        call_record.save()
    except:
        print "an error occured for ", row
    #import pdb;pdb.set_trace()

