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
from rest_framework.permissions import IsAuthenticated

from .models import SOTSadmin, SOTSCallRecord
from .serializers import SOTSAdminSerializer
from .utils import get_round_info_dict
from . import values_list,INFORMED, NOT_INFORMED

log = logging.getLogger('rssb')

class ObtainAuthTokenModified(ObtainAuthToken):
    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created =  Token.objects.get_or_create(user=user)

            log.debug('User login successfull for user %s' % user)
            return Response({'data': {'token': token.key}})
        log.debug('User login unsuccessful, errors %s' % serializer.errors)
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
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        
        common_filters = {'locked': False, 'overall_status': NOT_INFORMED}
        family_current_round = 1
        #indv_current_round = 1
        fetch_family_records = True
        data_set = []
        data = {}
        username = request.user.username
        # Family Records
        log.debug('Fetch record initiated by user %s' % username)
        for round_number in xrange(1,4):
            records_per_family = SOTSCallRecord.objects.exclude(familyid=0).filter(**common_filters)
            if records_per_family.filter(current_round=round_number).exists():
                records_per_family = records_per_family.values('familyid').annotate(dcount=Count('familyid')).order_by('-dcount')
                family_current_round = round_number
                break

        # Individual Records
        # for round_number in xrange(1,4):
        #     records = SOTSCallRecord.objects.filter(familyid=0).filter(**common_filters).order_by('ssrecid')
        #     round_user = 'round%s_user' % round_number
        #     custom = {'round%s_sotsuser__isnull' % round_number: True}
        #     indv_records = records.filter(current_round=round_number).filter(**custom)
        #     if indv_records.exists():
        #         indv_current_round = round_number
        #         break

        records = SOTSCallRecord.objects.filter(familyid=0).filter(**common_filters).order_by('ssrecid')
        round_1 = 1
        round_2 = 2
        round_3 = 3
        records_round1 = records.filter(current_round=round_1)
        records_round2 = records.filter(current_round=round_2)
        records_round3 = records.filter(current_round=round_3)

        if records_round1.exists():
            log.debug('round 1 records exists ')
            indv_records = records_round1
            indv_current_round = round_1
        elif records_round2.exists():
            log.debug('round 2 records exists')
            indv_records = records_round2
            indv_current_round = round_2
        elif records_round3.exists():
            log.debug('round 3 records exists ')
            indv_records = records_round3
            indv_current_round = round_3
        else:
            log.debug('No records found, all processed ')
            return Response({'data': []})

        log.debug('get request - user - %s, round %s' % (username, indv_current_round))
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
            record_result = indv_records.values(*values_list)
            record_result = record_result[0]
            record_result.update({'head': True})

            data_set.append(record_result)
            
        log.debug('Returning data set for get, round %s, user %s, data set %s' % (indv_current_round,
                   username, data_set))
        data['data'] = data_set#json.dumps(data_set)

        return Response(data)


class SOTSRecordUpdate(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        record_id = kwargs.get('record_id')
        payload = request.data.get('data')
        contacted_number = ''
        
        username = request.user.username
        log.debug('Update request initiated for record %s by user %s, payload %s' % (record_id,
                   username, payload))
        
        try:
            payload = json.loads(payload)
        except Exception, error:
            log.error('Error loading the payload for record %s error %s, username %s, payload %s' % (record_id,
                       error, username, payload))
        data_set = payload.get('data')
        # TODO: uncomment for family records and user exists()
        family_records = None #SOTSCallRecord.objects.filter(familyid=record_id)
        if family_records:
            
            for data in data_set:
                indv_record = family_records.filter(ssrecid=data.get('ssrecid'))
                current_round = data.get('current_round', 1)
                call_status_dict = get_round_info_dict(data)
                updated_record = indv_record.update(**call_status_dict)
                if INFORMED in call_status_dict.itervalues():
                    contacted_number = data.get('contacted_number')

            if contacted_number:
                family_records.update(overall_status=INFORMED)

            round_info = {'round%d_timestamp' % current_round: datetime.datetime.now(),
                          'round%d_sotsuser' % current_round: request.user,
                          'current_round': current_round + 1,
                          'locked': False,
                          'contacted_number': contacted_number
                          }
            family_records.update(**round_info)
                # if we are here, it means that the status is informed, so update overall status

        else:
            indv_record = SOTSCallRecord.objects.filter(ssrecid=record_id, locked=True)
            
            if indv_record.exists():
                log.debug('Found the indv record for update request payload %s, username %s' % (data_set,
                          username))
                for data in data_set:
                    current_round = data.get('current_round')
                    call_status_dict = get_round_info_dict(data)
                    log.debug('call status dict for payload %s, username %s, dict %s' % (data_set, username,
                               call_status_dict))
                    updated_record = indv_record.update(**call_status_dict)
                    
                    if INFORMED in call_status_dict.itervalues():
                        log.debug('Caller informed for payload %s, username %s' %(data, username))
                        contacted_number = data.get('contacted_number')

                if contacted_number:
                    log.debug('Updating the record status as informed payload %s, username %s' %(data_set,
                              username))
                    indv_record.update(overall_status=INFORMED)
                

                log.debug('***************contacted_number %s*****' % contacted_number)
                round_info = {'round%d_timestamp' % current_round: datetime.datetime.now(),
                              'round%d_sotsuser' % current_round: request.user,
                              'current_round': current_round + 1,
                              'locked': False,
                              'contacted_number': contacted_number
                              }
                log.debug('updating the round info for payload %s, username %s, round info %s' % (data_set,
                          username, round_info))
                indv_record.update(**round_info)
                message = 'Record with id %s updated successfully' % record_id
            else:
                log.debug('The record does not exist for record id %s, data %s, username %s' % (record_id, data_set,
                           username))
                # TODO: change the status to 404
                message  = 'Record with id %s either does not exist or is not locked' % record_id

        return Response({'data': {'message': message}})


class SOTSRecordLock(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)


    def put(self, request, *args, **kwargs):
        record_id = kwargs.get('record_id')
        log.debug('Lock call initiated for %s' % record_id)
        username = request.user.username
        # TODO: uncomment this for family records and check exists() queryset
        family_records = None #SOTSCallRecord.objects.filter(familyid=record_id)
        if family_records:
            family_records.update(locked=True)

        else:
            indv_record = SOTSCallRecord.objects.filter(ssrecid=record_id, locked=False)
            if indv_record.exists():
                log.debug('lock call successfull by username %s for record %s' % (username, record_id))
                indv_record.update(locked=True)
                message = 'Record locked for id %s' % record_id
            else:
                # TODO: change the status to 404
                message = 'Record with id %s either does not exist or is already locked' % record_id

        return Response({'data': {'message': message}})


class SOTSRecordUnLock(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)


    def put(self, request, *args, **kwargs):
        record_id = kwargs.get('record_id')
        log.debug('Unlock call initiated for %s' % record_id)
        username = request.user.username
        # TODO: uncomment this for family records and check exists() queryset
        family_records = None #SOTSCallRecord.objects.filter(familyid=record_id)
        if family_records:
            family_records.update(locked=False)

        else:
            indv_record = SOTSCallRecord.objects.filter(ssrecid=record_id, locked=True)
            if indv_record.exists():
                log.debug('unlock call successfull by username %s for record %s' % (username, record_id))
                indv_record.update(locked=False)
                message = 'Record unlocked for id %s' % record_id
            else:
                # TODO: change the status to 404
                message = 'Record with id %s either does not exist or is already unlocked' % record_id

        return Response({'data': {'message': message}})
