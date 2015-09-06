from rest_framework import serializers

from .models import SOTSadmin, SOTSCallRecord

class SOTSAdminSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SOTSadmin
        fields = ('firstname', 'lastname', 'username', 'password')