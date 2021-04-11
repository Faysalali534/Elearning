from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from accounts.models import Test

import os
print(os.path)


class Command(BaseCommand):
    help = 'The help information for this command.'

    def add_arguments(self, parser):
        parser.add_argument('number', type=int, help="total dummy tests to create")
        parser.add_argument('--option1', default="default", help='option1 optional value')

    def handle(self, *args, **options):
        print('Command: dummy test')
        print(f'Total dummy users : {options["number"]}')
        print(f'Option1 : {options["option1"]}')

        if options["number"] > 0:
            self.stdout.write(self.style.SUCCESS("We can Create these dummies"))
        else:
            raise CommandError('Wrong Input')

        try:
            for i in range(options["number"]):
                test = Test.objects.create(my_time=timezone.now())
                test.save()
        except:
            print('Cant create Test')

