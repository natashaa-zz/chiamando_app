from django.conf.urls import patterns, include, url

from .routers.core import root_router
from .views import SOTSRecordView, SOTSRecordUpdate, SOTSRecordLock, obtain_auth_token
from .views import SOTSRecordUnLock



urlpatterns = patterns(
    '',
    url(r'^', include(root_router.urls)),
    url(r'^login/', obtain_auth_token),
    url(
        r'^sotsrecord/$',
        SOTSRecordView.as_view(),
        name='sots-record'
    ),
    url(
        r'^sotsrecord/record_id/(?P<record_id>\d+)/$',
        SOTSRecordUpdate.as_view(),
        name='update_sots_call_record'
    ),
    url(
        r'^sotsrecord/lock/record_id/(?P<record_id>\d+)/$',
        SOTSRecordLock.as_view(),
        name='lock_sots_call_record'
    ),
    url(
        r'^sotsrecord/unlock/record_id/(?P<record_id>\d+)/$',
        SOTSRecordUnLock.as_view(),
        name='unlock_sots_call_record'
    ),

)