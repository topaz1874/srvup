import django.dispatch

page_view = django.dispatch.Signal(providing_args=['path'])