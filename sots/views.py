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
        
        data_set = []
        data = {}
        common_filters = {'locked': False, 'overall_status': NOT_INFORMED}
        non_family_filter = {'familyid': 0}
        family_current_round = 1
        username = request.user.username

        log.debug('get request - user - %s' % username)

        for round_number in xrange(1,4):
            all_records = SOTSCallRecord.objects.filter(current_round=round_number, **common_filters)
            records = all_records.filter(**non_family_filter).order_by('ssrecid')
            current_round = round_number
            if records.exists():
                log.debug('User %s, current_round %s, notify individual' %(username, current_round))
                break
            else:
                records = all_records.exclude(**non_family_filter).order_by('ssrecid')
                if records.exists():
                    log.debug('User %s, current_round %s, notify family' %(username, current_round))
                    break

        if records.exists():
            record_result = records.values(*values_list)
            record_result = record_result[0]
            data_set.append(record_result)
            log.debug('Returning data set for get, round %s, user %s, data set %s'
                      % (current_round, username, data_set))
        else:
            log.debug('No records found, all processed !!!')
            
        data['data'] = data_set

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
        record = SOTSCallRecord.objects.filter(ssrecid=record_id, locked=True)

        if record.exists():
            family_id = record[0].familyid
            log.debug('Found the indv record for update request payload %s, username %s' % (data_set,
                      username))
            if family_id:
                family_records = SOTSCallRecord.objects.filter(familyid=family_id)
            for data in data_set:
                current_round = data.get('current_round')
                call_status_dict = get_round_info_dict(data)
                log.debug('call status dict for payload %s, username %s, dict %s' % (data_set, username,
                           call_status_dict))
                updated_record = record.update(**call_status_dict)

                if INFORMED in call_status_dict.itervalues():
                    log.debug('Caller informed for payload %s, username %s' %(data, username))
                    contacted_number = data.get('contacted_number')

            if contacted_number:
                record.update(overall_status=INFORMED)
                if family_id:
                    family_records.update(overall_status=INFORMED)
                log.debug('Updating the record status as informed payload %s, username %s, '
                          'record id %s, family id %s' %(data_set, username, record_id, family_id))
            
            round_info = {
                'round%d_timestamp' % current_round: datetime.datetime.now(),
                'round%d_sotsuser' % current_round: request.user,
                'current_round': current_round + 1,
            }
            unlock_info = {
                'locked': False,
                'contacted_number': contacted_number
            }

            log.debug('updating the round info for payload %s, username %s, round info %s' % (data_set,
                      username, round_info))
            record.update(**round_info)
            record.update(**unlock_info)
            if family_id:
                family_records.update(**unlock_info)
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
        username = request.user.username
        log.debug('Lock call initiated for %s by user %s' % (record_id, username))

        # TODO: uncomment this for family records and check exists() queryset
        record = SOTSCallRecord.objects.filter(ssrecid=record_id, locked=False)
        if record.exists():
            message = 'Record locked for id %s' % record_id
            family_id = record[0].familyid
            log.debug('lock call successfull by username %s for record %s, familyid %s'
                      % (username, record_id, family_id))
            if family_id:
                SOTSCallRecord.objects.filter(familyid=family_id).update(locked=True)
            else:
                record.update(locked=True)
        else:
            # TODO: change the status to 404
            message = 'Record with id %s either does not exist or is already locked' % record_id

        return Response({'data': {'message': message}})


class SOTSRecordUnLock(APIView):
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):
        record_id = kwargs.get('record_id')
        username = request.user.username
        log.debug('Unlock call initiated for %s by username %s' % (record_id, username))

        # TODO: uncomment this for family records and check exists() queryset
        record = SOTSCallRecord.objects.filter(ssrecid=record_id, locked=True)
        if record.exists():
            message = 'Record unlocked for id %s' % record_id
            family_id = record[0].familyid
            log.debug('Unlock call successfull by username %s for record %s, familyid %s'
                      % (username, record_id, family_id))
            if family_id:
                SOTSCallRecord.objects.filter(familyid=family_id).update(locked=False)
            else:
                record.update(locked=False)
        else:
            # TODO: change the status to 404
            message = 'Record with id %s either does not exist or is already unlocked' % record_id

        return Response({'data': {'message': message}})
