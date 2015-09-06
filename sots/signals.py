import django.dispatch

update_callrecord = django.dispatch.Signal(providing_args=["instance"])