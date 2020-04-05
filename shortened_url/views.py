from django.http import HttpResponsePermanentRedirect
from rest_framework import status
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from shortened_url.exceptions import SubpartAlreadyTakenException
from shortened_url.models import ShortenedURL
from shortened_url.serializers import (
    ShortenedURLCreateSerializer,
    ShortenedURLSubpartSerializer,
    ShortenedURLRetrieveSerializer
)
from shortened_url.services import ShortenedURLService


class ShortenedURLListCreateAPIView(ListCreateAPIView):
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLRetrieveSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            subpart = ShortenedURLService.shorten_url(serializer.data, request.session.session_key)
            generated_url = request.build_absolute_uri(f'/{subpart}/')

            return Response(
                {'short_url': generated_url},
                status=status.HTTP_201_CREATED
            )

        except SubpartAlreadyTakenException:
            return Response(
                {'message': 'Subpart is already taken.'},
                status=status.HTTP_400_BAD_REQUEST
            )

    def get_queryset(self):
        return super().get_queryset().filter(user_id=self.request.session.session_key)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ShortenedURLCreateSerializer
        return self.serializer_class

    def get_serializer_context(self):
        return {'request': self.request}
    

class RedirectToLongURLAPIView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = ShortenedURLSubpartSerializer(data=kwargs)
        serializer.is_valid(raise_exception=True)

        long_url = ShortenedURLService.get_long_url(serializer.data['subpart'])
        if long_url is None:
            return Response({'message': 'Record not found.'}, status=status.HTTP_404_NOT_FOUND)

        return HttpResponsePermanentRedirect(long_url)
