from django import forms

from api import models


class SearchForm(forms.Form):
    date_from = forms.DateField(required=False)
    date_to = forms.DateField(required=False)
    os = forms.MultipleChoiceField(choices=(), required=False)
    country = forms.MultipleChoiceField(choices=(), required=False)
    channel = forms.MultipleChoiceField(choices=(), required=False)
    sort = forms.ChoiceField(
        choices=[(x.name, x.name) for x in models.DataSet._meta.fields] +
                [('CPI', 'CPI')],
        required=False,
    )
    order = forms.CharField(required=False)
    group_by = forms.MultipleChoiceField(
        choices=((x.name, x.name) for x in models.DataSet._meta.fields),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['os'].choices = (
            (x, x)
            for x in models.DataSet.objects.all().values_list(
                'os', flat=True,
            ).distinct()
        )
        self.fields['country'].choices = (
            (x, x)
            for x in models.DataSet.objects.all().values_list(
                'country', flat=True,
            ).distinct()
        )
        self.fields['channel'].choices = (
            (x, x)
            for x in models.DataSet.objects.all().values_list(
                'channel', flat=True,
            ).distinct()
        )
