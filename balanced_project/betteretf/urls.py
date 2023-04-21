from django.urls import path
from django.views.generic import RedirectView

from . import views
from .views import tickerSearchView

urlpatterns = [
    path('', tickerSearchView.as_view(), name='ticker_search'),
]
