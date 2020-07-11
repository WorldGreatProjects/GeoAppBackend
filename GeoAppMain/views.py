from django.http import HttpResponse
from django.views.generic import View

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
    JSON_FAILED = {"status": "failed",
                   "message": ""}

    @classmethod
    def check_request_method(cls, request):

        if request.method == 'GET':
            response = str(cls.get(request))
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
        except Profile.DoesNotExist:
            cls.JSON_FAILED["message"] = "User does not exist"
            return cls.JSON_FAILED
        return json.dumps(response)

    @classmethod
    def post(cls, request):

        try:
            request_json = json.loads(str(request.body.decode('utf-8')))
        except ValueError:
            cls.JSON_FAILED["message"] = "Error in json from client"
            return cls.JSON_FAILED

        user = Profile(email=request_json['email'],
                       username=request_json['user_name'],
                       string_id=request_json['id'],
                       description=request_json['description'])
        try:
            user.save()
        except Exception:
            cls.JSON_FAILED["message"] = "User can't be save. This email or nickname exists"
            return cls.JSON_FAILED

        return cls.JSON_SUCCESS

    @classmethod
    def put(cls, request):

        request_json = json.loads(str(request.body.decode('utf-8')))
        try:
            user = Profile.objects.get(string_id__exact=request_json['id'])
        except Profile.DoesNotExist:
            cls.JSON_FAILED["message"] = "User does not exist"
            return cls.JSON_FAILED

        user.email = request_json['email']

        try:
            user.save()
        except Exception as e:
            cls.JSON_FAILED["error"] = "User can't be save. This email or nickname exists"
            return cls.JSON_FAILED

        return cls.JSON_SUCCESS
