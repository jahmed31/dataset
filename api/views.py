from .models import DataSet
from django.db.models import (
    Sum,
    F,
    FloatField
)
from django.http import JsonResponse
from django.views.generic import ListView

from api import forms


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
        form = forms.SearchForm(data=request.GET)
        if not form.is_valid():
            return JsonResponse(
                status=400,
                data={'errors': form.errors},
                safe=False
            )

        model_filters = dict()
        select_list = set()
        # date from filter
        if form.cleaned_data.get('date_from'):
            model_filters['date__gte'] = form.cleaned_data['date_from']
        # date to filter
        if form.cleaned_data.get('date_to'):
            model_filters['date__lte'] = form.cleaned_data['date_to']
        # operating system filter
        if form.cleaned_data.get('os'):
            model_filters['os__in'] = form.cleaned_data['os']
        # country filter
        if form.cleaned_data.get('country'):
            model_filters['country__in'] = form.cleaned_data['country']
        # channel filter
        if form.cleaned_data.get('channel'):
            model_filters['channel__in'] = form.cleaned_data['channel']
        # group by column filter
        if form.cleaned_data.get('group_by'):
            select_list = form.cleaned_data['group_by']
        # getting records from database
        queryset = DataSet.objects.values(*select_list).annotate(
            impressions=Sum(F('impressions')),
            clicks=Sum(F('clicks')),
            revenue=Sum(F('revenue')),
            spends=Sum(F('spend'), output_field=FloatField()),
            CPI=(
                Sum(F('spend'), output_field=FloatField())
                /
                Sum(F('installs'), output_field=FloatField())
            )
        ).filter(**model_filters)
        # sorted column name
        if form.cleaned_data.get('sort'):
            order_by = form.cleaned_data['sort']
            if form.cleaned_data.get('order', 'asc') == 'desc':
                order_by = '-' + order_by
            # sorting data ascending/descending
            queryset = queryset.order_by(order_by)

        try:
            total_count = queryset.count()
            response = {'status': 200, 'data': list(queryset),
                        'total': total_count, 'message': 'Success'}
        except Exception as exe:
            response = {'status': 406, 'data': [], 'message': 'Bad Request',
                        'error': str(exe)}

        return JsonResponse(response, safe=False)
