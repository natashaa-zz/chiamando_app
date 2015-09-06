from django.contrib import admin
from .models import SOTSadmin, SOTSCallRecord
from .signals import update_callrecord

# Register your models here

class SOTSadminSite(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'username')

class SOTSCallRecordAdmin(admin.ModelAdmin):
    list_display = ('ssrecid', 'familyid', 'firstname', 'middlename', 'lastname', 'contacted_number', 'overall_status')

    fieldsets = (
        ('User Info', {
            'fields': 
                (
                    ('ssrecid', 'familyid', 'firstname', 'middlename', 'lastname'),
                    ('mobile1', 'mobile2', 'landline'),
                    ('emergency_contact1_name', 'emergency_contact1'),
                    ('emergency_contact2_name', 'emergency_contact2')
                )
        }),
        ('Extra Info', {
            'fields':
                (
                    ('locked', 'overall_status', 'current_round'),
                    ('contacted_number', 'remarks')
                )
        }),
        ('Round 1 Info', {
            'fields':
                (
                    ('round1_mobile1_status', 'round1_mobile2_status', 'round1_landline_status'),
                    ('round1_timestamp', 'round1_sotsuser')
                )
        }),
        ('Round 2 Info', {
            'fields':
                (
                    ('round2_mobile1_status', 'round2_mobile2_status', 'round2_landline_status'),
                    ('round2_timestamp', 'round2_sotsuser')
                )
        }),
        ('Round 3 Info', {
            'fields':
                (
                    ('round3_mobile1_status', 'round3_mobile2_status', 'round3_landline_status'),
                    ('round3_emergency_contact1_status', 'round3_emergency_contact2_status'),
                    ('round3_timestamp', 'round3_sotsuser')
                )
        })
    )

    def save_model(self, request, obj, form, change):
        #import pdb;pdb.set_trace()
        status_informed = (obj.round1_mobile1_status == 'I' or obj.round1_mobile2_status == 'I'
                           or obj.round1_landline_status == 'I' or obj.round2_mobile1_status == 'I'
                           or obj.round2_mobile2_status == 'I' or obj.round2_landline_status == 'I'
                           or obj.round3_mobile1_status == 'I' or obj.round3_mobile2_status == 'I'
                           or obj.round3_landline_status == 'I' or obj.round3_emergency_contact1_status == 'I'
                           or obj.round3_emergency_contact1_status == 'I')

        print "************", status_informed
        #import pdb;pdb.set_trace()
        if obj.familyid and status_informed:
            obj.overall_status = 'I'
        
        obj.save()
        # trigger a signal
        update_callrecord.send(sender=obj.__class__, instance=obj)
        

admin.site.register(SOTSadmin, SOTSadminSite)
admin.site.register(SOTSCallRecord, SOTSCallRecordAdmin)
