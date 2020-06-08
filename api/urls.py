from django.urls import path
from .views import SearchDataSet


urlpatterns = [
    path('filter_data', SearchDataSet.as_view())
]
