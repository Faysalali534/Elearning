from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from accounts.models import UserProfile
import os
print(os.path)


class Command(BaseCommand):
    help = 'The help information for this command.'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help="username to create")
        parser.add_argument('name', type=str, help="Name value")
        parser.add_argument('--option1', default="default", help='option1 optional value')

    def handle(self, *args, **options):
        print('Command: mycommand')
        print(f'id : {options["username"]}')
        print(f'name : {options["name"]}')
        print(f'Option1 : {options["option1"]}')

        if len(options["username"]) > 5:
            self.stdout.write(self.style.SUCCESS("Length is alright"))
        else:
            raise CommandError('Length short')

        try:
            User.objects.get(username=options["username"])
        except ObjectDoesNotExist:
            user = User.objects.create(username=options["username"])
            user.first_name = 'death'
            user.last_name = 'racer'
            user.email = 'racer@gmail.com'
            user.set_password('Vend1213')
            user.save()
            userinfo = UserProfile.objects.create(user=user)
            userinfo.phone_number = "03204432250"
            userinfo.location = "Liberty Gate"
            userinfo.user_type = 'professor'
            userinfo.save()

            group_get, created = Group.objects.get_or_create(name=userinfo.user_type)
            if not created:
                user.groups.add(group_get)
            UserProfile.user = user
