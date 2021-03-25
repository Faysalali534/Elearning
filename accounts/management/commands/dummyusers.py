from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
import os
print(os.path)


class Command(BaseCommand):
    help = 'The help information for this command.'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help="total dummy users to create")
        parser.add_argument('--option1', default="default", help='option1 optional value')

    def handle(self, *args, **options):
        print('Command: dummy users')
        print(f'Total dummy users : {options["number"]}')
        print(f'Option1 : {options["option1"]}')

        if options["number"] > 0:
            self.stdout.write(self.style.SUCCESS("We can Create these dummies"))
        else:
            raise CommandError('Wrong Input')

        try:
            for i in range(options["number"]):
                user = User.objects.create()
                user.first_name = 'Test'
                user.last_name = 'racer'
                user.email = 'racer@gmail.com'
                user.set_password('Vend1213')
                user.save()
        except:
            print('Cant create User')

