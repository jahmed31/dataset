import csv
import datetime

from django.core.management.base import BaseCommand, CommandError
from api.models import DataSet


class Command(BaseCommand):
    """
    Class to add dataset csv in to django model
    """
    help = 'Adding the dataset csv in database'

    def add_arguments(self, parser):
        """
        Function to add given file path argument into parser object
        :param parser: parser object (obj)
        :return: None
        """
        parser.add_argument('csv_path', nargs='+', type=str)

    def handle(self, *args, **options):
        """
        Function to insert csv data into database
        :param args: empty
        :param options: command line argument(s) (dict)
        """
        dataset_objs = DataSet.objects.all()
        if dataset_objs:
            dataset_objs.delete()
        dataset_csv = options['csv_path'][0]
        try:
            with open(dataset_csv, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    dataset_obj = DataSet()
                    dataset_obj.date = self.format_date(row['date'])
                    dataset_obj.channel = row['channel']
                    dataset_obj.country = row['country']
                    dataset_obj.os = row['os']
                    dataset_obj.impressions = row['impressions']
                    dataset_obj.clicks = row['clicks']
                    dataset_obj.installs = row['installs']
                    dataset_obj.spend = row['spend']
                    dataset_obj.revenue = row['revenue']
                    dataset_obj.save()
                    message = f'Successfully Inserted {row}'
                    self.stdout.write(self.style.SUCCESS(message))
        except IOError:
            raise CommandError(f'Dataset file {dataset_csv} does not exist')
        except KeyError:
            raise CommandError(f'Cannot access dictionary key')

    @staticmethod
    def format_date(date):
        return datetime.datetime.strptime(date, '%Y-%m-%d').date()
