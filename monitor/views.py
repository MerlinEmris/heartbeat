import json

from django.shortcuts import HttpResponse, render
from django.contrib.auth.models import User

from rest_framework import permissions, serializers, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Site
from .tasks import site_pulse_checker
from .utils import scanner

class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        exclude = ('user',)

class SiteViewSets(ModelViewSet):
    serializer_class = SiteSerializer
    queryset = Site.objects.all()
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Site.objects.all()
        else:
            return Site.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)




class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class ScanAPIView(APIView):
    """
    For scanning urls of user.

    * Log in to use this url
    """
    def get(self, request, format=None):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(request.user.username, {"type": "state.info",
                                                          "data": {'type': 'success', 'message':'Task started!'}})
        # sites = [site['url'] for site in list(Site.objects.filter(user=request.user).values('url'))]
        sites =[site for site in  list(Site.objects.filter(user=request.user).values('id','name','url'))]
        print(sites)
        site_pulse_checker.delay(sites,request.user.username)
        # async_to_sync(scanner)(sites,request.user)
        return Response(status=status.HTTP_200_OK, data={'message': "Success"})

def main(request):
    return render(request, 'index.html')

def not_found_api(request):
    return HttpResponse(status=404,  content="Not Found",  content_type="text/plain",  charset="utf-8")