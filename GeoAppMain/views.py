from django.views.generic import View

from .models import *
from .utils import *

import json

JSON_SUCCESS = {"status": "success",
                "message": ""}

JSON_FAILED = {"status": "failed",
               "message": ""}


def hello(request):
    return HttpResponse('Welcome to GeoApp start page')


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

    @staticmethod
    def check_request_method(request, string_id):
        if request.method == 'GET':
            response = str(UserController.get(request, string_id))
            return HttpResponse(response)
        if request.method == 'POST':
            response = str(UserController.post(request, string_id))
            return HttpResponse(response)
        if request.method == 'PUT':
            response = str(UserController.put(request, string_id))
            return HttpResponse(response)
        if request.method == 'DELETE':
            response = str(UserController.delete(request, string_id))
            return HttpResponse(response)

    @classmethod
    def get(cls, request, string_id):
        try:
            user = Profile.objects.get(id__exact=string_id)
            response = {'id': user.id,
                        'email': user.email,
                        'username': user.username,
                        'name': user.name,
                        'desc': user.desc,
                        'subs': user.subs,
                        'followers': user.followers,
                        'pic': user.pic}

        except Profile.DoesNotExist:
            JSON_FAILED["message"] = "User does not exist"
            return JSON_FAILED
        return json.dumps(response)

    @classmethod
    def post(cls, request, string_id):
        try:
            request_json = json.loads(str(request.body.decode('utf-8')))
        except ValueError:
            JSON_FAILED["message"] = "Error in json from client"
            return JSON_FAILED

        user = Profile(email=request_json['email'],
                       username=request_json['username'],
                       id=string_id,
                       password=request_json['password'])
        try:
            user.save()
        except Exception:
            JSON_FAILED["message"] = "User can't be save. This email or nickname exists"
            return JSON_FAILED

        return JSON_SUCCESS

    @classmethod
    def put(cls, request, string_id):
        request_json = json.loads(str(request.body.decode('utf-8')))
        try:
            user = Profile.objects.get(id__exact=string_id)
        except Profile.DoesNotExist:
            JSON_FAILED["message"] = "User does not exist"
            return JSON_FAILED

        user.password = request_json["password"]
        user.username = request_json["username"]
        user.desc = request_json["desc"]
        user.email = request_json["email"]
        user.name = request_json["name"]

        try:
            user.save()
        except Exception as e:
            JSON_FAILED["error"] = "User can't be save. This email or nickname exists"
            return JSON_FAILED

        return JSON_SUCCESS

    @classmethod
    def delete(cls, request, string_id):
        try:
            user = Profile.objects.get(id__exact=string_id)
        except Profile.DoesNotExist:
            JSON_FAILED["message"] = "User does not exist"
            return JSON_FAILED
        user.delete()
        JSON_SUCCESS["message"] = "User was deleted"
        return JSON_SUCCESS


class UserLogin(View):

    @classmethod
    def post(cls, request):
        try:
            request_json = json.loads(str(request.body.decode('utf-8')))
        except ValueError:
            JSON_FAILED["message"] = "Error in json from client"
            return HttpResponse(str(JSON_FAILED))

        try:
            user_from_username = Profile.objects.get(username__exact=request_json["username"])
        except Profile.DoesNotExist:
            JSON_FAILED["message"] = "User does not exist"
            return HttpResponse(str(JSON_FAILED))

        if user_from_username.password == request_json["password"]:
            response = {'id': user_from_username.id,
                        'email': user_from_username.email,
                        'username': user_from_username.username,
                        'desc': user_from_username.desc,
                        'name': user_from_username.name,
                        'password':user_from_username.password}
            return HttpResponse(str(json.dumps(response)))


class UserAction(View):

    @classmethod
    def post(cls, request, string_id):
        try:
            request_json = json.loads(str(request.body.decode('utf-8')))
        except ValueError:
            JSON_FAILED["message"] = "Error in json from client"
            return JSON_FAILED

        if request_json["action"] == "subscribe":
            try:
                user_that_subscribe = Profile.objects.get(id__exact=string_id)

                # user_that_subscribe it is new follower for user_add_follower
                user_add_follower = Profile.objects.get(id__exact=request_json["id"])
            except Profile.DoesNotExist:
                JSON_FAILED["message"] = "User does not exist"
                return JSON_FAILED

            user_add_follower.users_followers.add(user_that_subscribe)
            JSON_SUCCESS["message"] = "Subscribe success"
            return JSON_SUCCESS

        if request_json["action"] == "unsubscribe":
            try:
                user_that_unsubscribe = Profile.objects.get(id__exact=string_id)

                # user_that_unsubscribe it is old follower for user_delete_follower
                user_delete_follower = Profile.objects.get(id__exact=request_json["id"])
            except Profile.DoesNotExist:
                JSON_FAILED["message"] = "User does not exist"
                return JSON_FAILED

            user_that_unsubscribe.subs.delete(user_delete_follower)
            JSON_SUCCESS["message"] = "Unsubscribe success"
            return JSON_SUCCESS


class MarkController(View):

    @staticmethod
    def check_request_method(request, string_id):
        if request.method == 'GET':
            response = str(MarkController.get(request, string_id))
            return HttpResponse(response)
        if request.method == 'POST':
            response = str(MarkController.post(request, string_id))
            return HttpResponse(response)
        if request.method == 'PUT':
            response = str(MarkController.put(request, string_id))
            return HttpResponse(response)
        if request.method == 'DELETE':
            response = str(MarkController.delete(request, string_id))
            return HttpResponse(response)

    @classmethod
    def get(cls, request, string_id):

        try:
            user = Profile.objects.get(id__exact=string_id)
        except Profile.DoesNotExist:
            JSON_FAILED["message"] = "User does not exist"
            return JSON_FAILED

        friends = user.subs

        marks = []

        for friend in friends:
            try:
                friends_marks = Profile.objects.get(id__exact=friend).marks
            except Profile.DoesNotExist:
                JSON_FAILED["message"] = "User does not exist"
                return JSON_FAILED

            for friends_mark in friends_marks:
                mark = Mark.objects.get(id=friends_mark)
                mark_json = {'lon': mark.lon,
                             'lat': mark.lat,
                             'desc': mark.desc,
                             'owner_id': mark.owner_id,
                             'date': mark.date}
                marks.extend(json.dumps(mark_json))
        return marks

    @classmethod
    def post(cls, request, string_id):

        try:
            request_json = json.loads(str(request.body.decode('utf-8')))
        except ValueError:
            JSON_FAILED["message"] = "Error in json from client"
            return JSON_FAILED

        mark = Mark(lon=request_json['lon'],
                    lat=request_json['lat'],
                    desc=request_json['desc'])

        try:
            user = Profile.objects.get(id__exact=string_id)
        except Profile.DoesNotExist:
            JSON_FAILED["message"] = "User does not exist"
            return JSON_FAILED

        user.marks.add(mark)

        try:
            mark.save()
        except Exception:
            JSON_FAILED["message"] = "Mark can't be save."
            return JSON_FAILED

        return JSON_SUCCESS

    # Здесь в json должны приходить lon и lat метки помимо id пользователя
    @classmethod
    def put(cls, request, string_id):

        request_json = json.loads(str(request.body.decode('utf-8')))
        try:
            mark = Mark.objects.get(owner_id__exact=string_id)
        except Mark.DoesNotExist:
            JSON_FAILED["message"] = "Marks does not exist"
            return JSON_FAILED

        json_keys = request_json.keys()
        for key in json_keys:
            mark.key = request_json[key]

        if string_id == mark.owner_id:
            try:
                mark.save()
                JSON_SUCCESS["message"] = "Edition success"
                return JSON_SUCCESS
            except Exception as e:
                JSON_FAILED["error"] = "Mark can't be save. This email or nickname exists"
                return JSON_FAILED
        else:
            JSON_FAILED["error"] = "Only owner of the mark can edit it."
            return JSON_FAILED

    @classmethod
    def delete(cls, request, string_id):
        pass


class UserResetPassword(View):
    pass
