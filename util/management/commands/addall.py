from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        # call_command('addteams')
        call_command('addevents')
        call_command('addrankings')
        #  call_command('addmatches')
        #  call_command('addawards')
        #  call_command('addelo')
