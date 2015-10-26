from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User

from .signals import update_callrecord

CALL_STATUS = (
    ('I', 'Informed'),
    ('W', 'Wrong Number'),
    ('N', 'Not Reachable')
)

STATUS_CHOICES = (
    ('I', 'Informed'),
    ('NI', 'Not Informed')
)

# SOTSadmins
class SOTSadmin(models.Model):
    username = models.CharField(max_length=50, primary_key=True, db_index=True)#text
    password = models.CharField(max_length=50, db_index=True)#text
    firstname = models.CharField(max_length=50)#text
    lastname = models.CharField(max_length=50)#text

    def __str__(self):
        return self.username

    class Meta:
         verbose_name = "SOTS Admin"

# SOTS Call Records
class SOTSCallRecord(models.Model):
    ssrecid = models.IntegerField(primary_key=True, db_index=True)#number
    familyid = models.IntegerField(db_index=True)#nunber
    firstname = models.CharField(max_length=50,)#text
    middlename = models.CharField(max_length=50, null=True, blank=True)#text
    lastname = models.CharField(max_length=50, null=True, blank=True)#text
    mobile1 = models.CharField(max_length=15, null=True, blank=True)
    mobile2 = models.CharField(max_length=15, null=True, blank=True)
    landline = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact1_name = models.CharField(max_length=50, null=True, blank=True)#text
    emergency_contact1 = models.CharField(max_length=15, null=True, blank=True)
    emergency_contact2_name = models.CharField(max_length=50, null=True, blank=True)#text
    emergency_contact2 = models.CharField(max_length=15, null=True, blank=True)
    locked = models.BooleanField(default=False, db_index=True)#boolean
    overall_status = models.CharField(max_length=4, default='NI', choices=STATUS_CHOICES, db_index=True)
    current_round = models.IntegerField(default=1)
    round1_mobile1_status = models.CharField(max_length=4, choices=CALL_STATUS, null=True, blank=True,
                                             db_index=True)#choice
    round1_mobile2_status = models.CharField(max_length=4, choices=CALL_STATUS, null=True, blank=True,
                                             db_index=True)#choice
    round1_landline_status = models.CharField(max_length=4, choices=CALL_STATUS, null=True, blank=True,
                                              db_index=True)#choice
    round1_emergency_contact1_status = models.CharField(max_length=4, choices=CALL_STATUS, null=True, blank=True,
                                              db_index=True)
    round1_emergency_contact2_status = models.CharField(max_length=4, choices=CALL_STATUS, null=True, blank=True,
                                              db_index=True)
    round1_sotsuser = models.ForeignKey(User, null=True, blank=True, #on_delete=models.SET_NULL,
                                        related_name='round1_sotsuser')#foreignkey to sotsadmin
    round1_timestamp = models.DateTimeField(null=True, blank=True)#datetime
    round2_mobile1_status = models.CharField(max_length=4, choices=CALL_STATUS, null=True, blank=True,
                                             db_index=True)#choice
    round2_mobile2_status = models.CharField(max_length=4, choices=CALL_STATUS, null=True, blank=True,
                                             db_index=True)#choice
    round2_landline_status = models.CharField(max_length=4, choices=CALL_STATUS, null=True, blank=True,
                                              db_index=True)#choice
    round2_emergency_contact1_status = models.CharField(max_length=4, choices=CALL_STATUS, null=True, blank=True,
                                              db_index=True)#choice
    round2_emergency_contact2_status = models.CharField(max_length=4, choices=CALL_STATUS, null=True, blank=True,
                                              db_index=True)#choice
    round2_sotsuser = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                        related_name='round2_sotsuser')#foreignkey to sotsadmin
    round2_timestamp = models.DateTimeField(null=True, blank=True)#datetime
    round3_mobile1_status = models.CharField(max_length=4, choices=CALL_STATUS, null=True, blank=True,
                                             db_index=True)#choice
    round3_mobile2_status = models.CharField(max_length=4, choices=CALL_STATUS, null=True, blank=True,
                                             db_index=True)#choice
    round3_landline_status = models.CharField(max_length=4, choices=CALL_STATUS, null=True, blank=True,
                                              db_index=True)#choice
    round3_emergency_contact1_status = models.CharField(max_length=4, choices=CALL_STATUS, null=True, blank=True,
                                                        db_index=True)#choice
    round3_emergency_contact2_status = models.CharField(max_length=4, choices=CALL_STATUS, null=True, blank=True,
                                                        db_index=True)#choice
    round3_sotsuser = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                        related_name='round3_sotsuser')#foreignkey to sotsadmin
    round3_timestamp = models.DateTimeField(null=True, blank=True)#datetime
    contacted_number = models.CharField(max_length=15, null=True, blank=True)#number
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return '%s:%s:%s' % (self.ssrecid, self.firstname, self.contacted_number)

    class Meta:
         verbose_name = "SOTS Call Record"


@receiver(update_callrecord, sender=SOTSCallRecord)
def on_update_callrecord_change_overall_status(sender, instance, **kwargs):
    familyid = instance.familyid
    if instance.overall_status == 'I' and familyid:
        records = sender.objects.filter(familyid=instance.familyid)
        records.update(overall_status='I')

