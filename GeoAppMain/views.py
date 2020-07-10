from django.http import HttpResponse
from django.views.generic import View

import time
import traceback

from .models import *

import json


def hello(request):
    return HttpResponse('Welcome to GeoApp start page')


# @method_decorator(csrf_exempt, name='dispatch')
class Coordinate(View):

    @staticmethod
    def get(request):
        answer_dict = {
            "user": "AlexWolf",
            "coordX": 234.14739,
            "coordY": 324.12341
        }

        answer_json = json.dumps(answer_dict)
        return HttpResponse(answer_json)

    @staticmethod
    def post(request):
        print(request)
        return HttpResponse(request)


class UserController(View):
    JSON_SUCCESS = {"status": "success"}
    JSON_FAILED = {"status": "failed"}

    @classmethod
    def check_request_method(cls, request):

        if request.method == 'GET':
            response = cls.get(request)
            return HttpResponse(response)
        if request.method == 'POST':
            response = str(cls.post(request))
            return HttpResponse(response)
        if request.method == 'PUT':
            response = str(cls.put(request))
            return HttpResponse(response)

    @classmethod
    def get(cls, request):

        response = {}

        try:
            users = Profile.objects.get(string_id__exact="bef3af7c-41b2-4268-bedc-bfd6abd8f935")
            response = {'id': users.string_id,
                        'email': users.email,
                        'username': users.username,
                        'description': users.description}

        except Exception as e:
            print('Ошибка:\n', traceback.format_exc())
        return json.dumps(response)

    @classmethod
    def post(cls, request):

        try:
            request_json = json.loads(str(request.body.decode('utf-8')))
        except ValueError:
            return cls.JSON_FAILED

        user = Profile(email=request_json['email'],
                       username=request_json['user_name'],
                       string_id=request_json['id'],
                       description=request_json['description'])
        user.save()

        return cls.JSON_SUCCESS

    @classmethod
    def put(cls, request):

        request_json = json.loads(str(request.body.decode('utf-8')))
        try:
            user = Profile.objects.get(string_id__exact=request_json['id'])
        except Profile.DoesNotExist:
            return cls.JSON_FAILED

        user.email = request_json['email']

        user.save()

        return cls.JSON_SUCCESS
