from rest_framework import routers

from sots.views import *

root_router = routers.DefaultRouter()
root_router.register(r'sotsadmins', SOTSAdminViewSet)