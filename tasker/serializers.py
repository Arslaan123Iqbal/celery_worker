from rest_framework.serializers import ModelSerializer
from .models import ScrapeTask
class ScraperSerializer(ModelSerializer):
             class Meta:
                model = ScrapeTask
                fields = '__all__'