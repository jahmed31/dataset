import datetime

from .models import DataSet
from django.db.models import Sum, F, FloatField
from django.http import JsonResponse
from django.views.generic import ListView


class SearchDataSet(ListView):
    """
    List all searched filters data.
    """

    def get(self, request, *args, **kwargs):
        """
        API endpoint function to filter search results
        :param request: http request object (request obj)
        :return: json response list of dictionary (json)
        """
        db_columns = ['channel', 'country', 'os', 'impressions', 'clicks'
                      'installs', 'spend', 'revenue', 'date']
        model_filters = dict()
        select_list = set()
        order_by = ''
        # date from filter
        if request.GET.get('date-from'):
            date_from = request.GET['date-from']
            model_filters['date__gte'] = self.to_date_obj(date_from)
            select_list.add('date')
        # date to filter
        if request.GET.get('date-to'):
            date_to = request.GET['date-to']
            model_filters['date__lte'] = self.to_date_obj(date_to)
            select_list.add('date')
        # operating system filter
        if 'operating-system' in request.GET:
            os = request.GET.getlist('operating-system')
            model_filters['os__in'] = os
            select_list.add('os')
        # country filter
        if 'countries' in request.GET:
            model_filters['country__in'] = request.GET.getlist('countries')
            select_list.add('country')
        # channel filter
        if 'channel' in request.GET:
            model_filters['channel__in'] = request.GET.getlist('channel')
            select_list.add('channel')
        # sorted column name
        if request.GET.get('sort'):
            order_by = request.GET.get('sort')
            if order_by not in db_columns:
                message = f'Column {order_by} not exists'
                return JsonResponse(status=401, message=message, data=[])
        # sorted order
        if (request.GET.get('order') and
                request.GET.get('order') == 'descending'):
            order_by = '-' + order_by
        select_list = list(select_list)

        try:
            dataset_objs = DataSet.objects.values(
                *select_list
            ).annotate(CPI=Sum(F('spend'), output_field=FloatField()) /
            Sum(F('installs'), output_field=FloatField())).filter(
                **model_filters
            ).order_by(order_by)
            if 'date' in select_list:
                dataset_objs = self.format_date(dataset_objs)
            total_count = dataset_objs.count()
            response = {'status': 200, 'data': list(dataset_objs),
                        'total': total_count, 'message': 'Success'}
        except Exception as exe:
            response = {'status': 406, 'data': [], 'message': 'Bad Request',
                        'error': str(exe)}

        return JsonResponse(response)

    @staticmethod
    def format_date(data):
        """
        function to format date
        :param data: datetime object (obj)
        :return: list of queryset (queryset)
        """
        for row in data:
            row['date'] = datetime.datetime.strftime(row['date'], '%Y-%m-%d')
        return data

    @staticmethod
    def to_date_obj(date):
        """
        function to convert string to date object
        :param date: date (str)
        :return: list of date object (list)
        """
        return datetime.datetime.strptime(date, '%Y-%m-%d').date()
