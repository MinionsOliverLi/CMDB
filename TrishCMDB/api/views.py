from django.shortcuts import render
from django import views
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from utils import auth

import json


# Create your views here.

class Asset(views.View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        # print('before')
        ret = super(Asset, self).dispatch(request, *args, **kwargs)
        # print('after')
        return ret

    @method_decorator(auth.api_auth)
    def get(self, request, *args, **kwargs):
        """
        ssh、salt模式,获取资产信息。
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

    @method_decorator(auth.api_auth)
    def post(self, request, *args, **kwargs):
        """
        增加或更新资产信息
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        client_data = json.loads(json.loads(request.body.decode('utf-8')))
        #print(type(client_data))
        hostname = client_data['hostname']
        ret = {'code': 1000, 'message': '[%s]Update complete.' % hostname}

        return JsonResponse(ret)
