import datetime
import json
import logging

from django.shortcuts import render
from django.db.models import Count, Q
from rest_framework import viewsets
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from .models import SOTSadmin, SOTSCallRecord
from .serializers import SOTSAdminSerializer
from .utils import get_round_info_dict
from . import values_list

log = logging.getLogger('rssb')
class ObtainAuthTokenModified(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created =  Token.objects.get_or_create(user=serializer.validated_data['user'])

            return Response({'data': {'token': token.key}})
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

obtain_auth_token = ObtainAuthTokenModified.as_view()

class SOTSAdminViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows admins users to be viewed.
    """
    queryset = SOTSadmin.objects.all()
    serializer_class = SOTSAdminSerializer


class SOTSRecordView(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request, *args, **kwargs):
        
        common_filters = {'locked': False, 'overall_status': 'NI'}
        family_current_round = 0
        indv_current_round = 0
        fetch_family_records = True
        data_set = []
        data = {}
        # Family Records
        log.debug('in get request')
        for round_number in xrange(1,4):
            records_per_family = SOTSCallRecord.objects.exclude(familyid=0).filter(**common_filters)
            if records_per_family.filter(current_round=round_number).exists():
                records_per_family = records_per_family.values('familyid').annotate(dcount=Count('familyid')).order_by('-dcount')
                family_current_round = round_number
                break

        # Individual Records
        for round_number in xrange(1,4):
            records = SOTSCallRecord.objects.filter(familyid=0).filter(**common_filters)
            indv_records = records.filter(current_round=round_number)
            if indv_records.exists():
                indv_current_round = round_number
                break
        # If round for individuals is less, then we have to fetch individual records so one round
        # can be finished.
        if family_current_round > indv_current_round and (not records_per_family.exists() and indv_records.exists()):
            pass
         
        # TODO: put it in globalsettings   
        fetch_family_records = False
    
        if fetch_family_records:          
            for record in records_per_family:
                familyid = record.get('familyid')
                family_records = SOTSCallRecord.objects.filter(familyid=familyid).values(*values_list)  
            for record in family_records:
                if record.get('ssrecid') == record.get('familyid'):
                    record.update({'head': True})
                else:
                    record.update({'head': False})
                data_set.append(record)
        elif indv_records.exists():
            records = records.values(*values_list)
            record = records[0]
            record.update({'head': True})
            data_set.append(record)
        print data_set
        data['data'] = data_set
        return Response(data)


class SOTSRecordUpdate(APIView):
    renderer_classes = (JSONRenderer,)

    def put(self, request, *args, **kwargs):
        record_id = kwargs.get('record_id')
        payload = request.data.get('data')
        contacted_number = 0
        current_round = 1
        print "payload *** ", payload
        print "record_id *** ", record_id
        try:
            payload = json.loads(payload)
        except Exception, error:
            print "exception", error
        data_set = payload.get('data')
        # TODO: record_id should be in redis (locked state)
        family_records = SOTSCallRecord.objects.filter(familyid=record_id)
        if family_records.exists():
            
            for data in data_set:
                indv_record = family_records.filter(ssrecid=data.get('ssrecid'))
                current_round = data.get('current_round')
                call_status_dict = get_round_info_dict(data)
                updated_record = indv_record.update(**call_status_dict)
                if 'I' in call_status_dict.itervalues():
                    contacted_number = data.get('contacted_number')

            if contacted_number:
                family_records.update(overall_status='I')

            round_info = {'round%d_timestamp' % current_round: datetime.datetime.now(),
                          'round%d_sotsuser' % current_round: request.user.username,
                          'current_round': current_round + 1,
                          'locked': False
                          }
            family_records.update(**round_info)
                # if we are here, it means that the status is informed, so update overall status

        else:
            indv_record = SOTSCallRecord.objects.filter(ssrecid=record_id)
            print data_set
            if indv_record.exists():
                for data in data_set:
                    current_round = data.get('current_round')
                    call_status_dict = get_round_info_dict(data)
                    updated_record = indv_record.update(**call_status_dict)
                    
                    if 'I' in call_status_dict.itervalues():
                        contacted_number = data.get('contacted_number')

                if contacted_number:
                    indv_record.update(overall_status='I')
                    
                round_info = {'round%d_timestamp' % current_round: datetime.datetime.now(),
                              'round%d_sotsuser' % current_round: request.user.username,
                              'current_round': current_round + 1,
                              'locked': False
                              }
                indv_record.update(**round_info)

        return Response({'data': {'message': 'Records with id %s updated successfully' % record_id}})


class SOTSRecordLock(APIView):
    renderer_classes = (JSONRenderer,)

    def put(self, request, *args, **kwargs):
        record_id = kwargs.get('record_id')
        print "record_id *** ", record_id
        # TODO: record_id should be in redis (locked state)
        family_records = SOTSCallRecord.objects.filter(familyid=record_id)
        if family_records.exists():
            family_records.update(locked=True)

        else:
            indv_record = SOTSCallRecord.objects.filter(ssrecid=record_id)
            if indv_record.exists():
                
                indv_record.update(locked=True)

        return Response({'data': {'message': 'Records locked for id %s' % record_id}})
