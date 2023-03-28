from balanced.serializers import fundSerializer, Fund, HoldingsBreakdown, HoldingsSerializer
from balanced.serializers import SectorsBreakdown, SectorsSerializer
from balanced.serializers import ThreeYearHistorySerializer, ThreeYearHistory, yahooRawSerializer, YahooRaw
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.response import Response

# create yahooRaw viewset for API
class YahooRawView(viewsets.ModelViewSet):
    serializer_class = yahooRawSerializer
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        queryset = YahooRaw.objects.all()
        ticker = self.request.query_params.get('ticker')
        if ticker:
            queryset = queryset.filter(ticker=ticker)
        return queryset


@api_view(['POST'])
def YahooRawCreateView(request):
    serializer = yahooRawSerializer(data=request.json)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        print('Something went wrong with FunCreateView?!')


# create Fund viewset for API
class FundView(viewsets.ModelViewSet):
    queryset = Fund.objects.all()
    serializer_class = fundSerializer
    lookup_field = 'ticker'


@api_view(['POST'])
def FundCreateView(request):
    serializer = fundSerializer(data=request.json)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        print('Something went wrong with FunCreateView?!')


# create Holdings viewset for API
class HoldingsView(viewsets.ModelViewSet):
    queryset = HoldingsBreakdown.objects.all()
    serializer_class = HoldingsSerializer


@api_view(['POST'])
def HoldingsCreateView(request):
    serializer = HoldingsSerializer(data=request.json)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        print('something went wrong with HoldingsCreateView')


# create Sector viewset for API
class SectorsView(viewsets.ModelViewSet):
    queryset = SectorsBreakdown.objects.all()
    serializer_class = SectorsSerializer


@api_view(['POST'])
def SectorsCreateView(request):
    serializer = SectorsSerializer(data=request.json)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        print('something went wrong with SectorCreateView')


# create LastThreeMonths viewset for API
class ThreeYearHistoryView(viewsets.ModelViewSet):
    queryset = ThreeYearHistory.objects.filter()
    serializer_class = ThreeYearHistorySerializer


@api_view(['POST'])
def ThreeYearHistoryCreateView(request):
    serializer = ThreeYearHistorySerializer(data=request.json)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        print('something went wrong with ThreeYearHistoryCreateView')
