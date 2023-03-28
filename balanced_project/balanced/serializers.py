# used for REST API framework routing and converting models into views
from rest_framework import serializers
from betteretf.models import Fund, HoldingsBreakdown, SectorsBreakdown, ThreeYearHistory, YahooRaw

# yahooRaw class serializer
class yahooRawSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = YahooRaw
        fields = '__all__'


# serializer class for funds
class fundSerializer(serializers.ModelSerializer):
    holdings = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    sectors = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    history = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Fund
        fields = '__all__'


# serializer class for HoldingsBreakdown
class HoldingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HoldingsBreakdown
        fields = '__all__'


# serializer class for SectorBreakdown
class SectorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectorsBreakdown
        fields = '__all__'


# serializer class for LastThreeMonths
class ThreeYearHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreeYearHistory
        fields = '__all__'
