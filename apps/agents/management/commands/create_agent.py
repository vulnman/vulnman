import os
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from apps.agents.models import Agent


class Command(BaseCommand):
    help = 'Create new Agent'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str)
        parser.add_argument('agent_name', type=str)

    def handle(self, *args, **options):
        try:
            user = User.objects.get(username=options['username'])
        except User.DoesNotExist:
            raise CommandError("User {user} does not exist!".format(user=options['username']))
        agent = Agent.objects.create(name=options['agent_name'], user=user)
        self.stdout.write(self.style.SUCCESS('Successfully created agent with key "%s"' % agent.key))

