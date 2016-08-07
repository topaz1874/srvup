from django.dispatch import Signal

become_member = Signal(providing_args=['month','year'])