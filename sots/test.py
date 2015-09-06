from .models import SOTSCallRecord

data = {}
records_per_family = SOTSCallRecord.objects.exclude(familyid=0).filter(
    locked=False).values('familyid').annotate(dcount=Count('familyid')).order_by('-dcount')
if not records_per_family.exists():
    records = SOTSCallRecord.objects.filter(familyid=0)
    if records.exists():
        data[records[0].ssrecid] = {'ssrecid': records[0].ssrecid, 'familyid': records.familyid}
else:

    for record in records_per_family:
        familyid = record.get('familyid')
        family_records = SOTSCallRecord.objects.filter(familyid=familyid)
        data[familyid] = []
        break
    data_set = []
    for record in family_records:
        data_set.append({'ssrecid': record.ssrecid, 'familyid': record.familyid})
    print data_set