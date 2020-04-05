from rest_framework import serializers

from shortened_url.models import ShortenedURL


class ShortenedURLCreateSerializer(serializers.Serializer):
    subpart = serializers.CharField(max_length=255, required=False)
    long_url = serializers.URLField(required=True)


class ShortenedURLRetrieveSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = ShortenedURL
        fields = ['long_url', 'short_url', 'created_at']

    def get_short_url(self, obj):
        return self.context['request'].build_absolute_uri(f'/{obj.subpart}/')


class ShortenedURLSubpartSerializer(serializers.Serializer):
    subpart = serializers.CharField(max_length=255, required=False)
