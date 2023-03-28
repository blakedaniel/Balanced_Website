"""balanced URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

# used to route urls from another URLconf file, see line 36
from django.urls import include

# used to redirect page urls to another urls
from django.views.generic import RedirectView

# used to let the development server serve static files like css, java, images, etc., see line 41
from django.conf import settings
from django.conf.urls.static import static

# used for REST API framework routing and converting models into views
from rest_framework import routers

from balanced.views import FundView, FundCreateView, HoldingsView, HoldingsCreateView, SectorsView, SectorsCreateView
from balanced.views import ThreeYearHistoryView, ThreeYearHistoryCreateView
from balanced.views import YahooRawView, YahooRawCreateView
from betteretf.views import HomeView

urlpatterns = [
    path("admin/", admin.site.urls),
]


# adds the translibrary app to pattern matching
# makes /translibrary/ the index/home page via redirect
urlpatterns += [
    path('betteretf/', HomeView),
    path('', RedirectView.as_view(url='api/', permanent=True)),
]


# used to let the development server serve static files like css, java, images, etc.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'fund', FundView, )
router.register(r'holdings', HoldingsView)
router.register(r'sectors', SectorsView)
router.register(r'ThreeYearHistory', ThreeYearHistoryView)
router.register(r'yahooraw', YahooRawView, basename='yahooraw')

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns += [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/fund/<str:ticker>/', include(router.urls)),

]
