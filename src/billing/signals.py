from django.dispatch import Signal

become_member = Signal(providing_args=['month','year'])

membership_date_update = Signal(providing_args=['new_date_start',])