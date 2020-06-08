import csv
import datetime

from django.core.management.base import BaseCommand, CommandError
from api.models import DataSet


class Command(BaseCommand):
    """
    Class to add dataset csv in to django model
    """
    help = """
    Populates DataSet model using the provided csv file. Columns inside csv
    should have following order.
    date,channel,country,os,impressions,clicks,installs,spend,revenue
    """

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

        # delete all the existing records to refresh the database
        DataSet.objects.all().delete()
        # getting dataset.csv
        dataset_csv = options['csv_path'][0]

        try:
            with open(dataset_csv, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                datasets = []
                for row in csv_reader:
                    row['date'] = self.format_date(row['date'])
                    datasets.append(DataSet(**row))
                # doing bulk insertion in database
                DataSet.objects.bulk_create(datasets)
                message = f'Successfully populated DataSet csv'
                # on successful insertion message display on command line
                self.stdout.write(self.style.SUCCESS(message))
        except IOError:
            raise CommandError(f'Dataset file {dataset_csv} does not exist')
        except KeyError:
            raise CommandError(f'Cannot access dictionary key')

    @staticmethod
    def format_date(date):
        return datetime.datetime.strptime(date, '%Y-%m-%d').date()
