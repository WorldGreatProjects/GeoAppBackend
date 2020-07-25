from django.http import HttpResponse

from abc import ABC, abstractmethod


class ObjectControllerMixin(ABC):

    def check_request_method(self, request, string_id):
        if request.method == 'GET':
            response = str(self.get(request, string_id))
            return HttpResponse(response)
        if request.method == 'POST':
            response = str(self.post(request, string_id))
            return HttpResponse(response)
        if request.method == 'PUT':
            response = str(self.put(request, string_id))
            return HttpResponse(response)
        if request.method == 'DELETE':
            response = str(self.delete(request, string_id))
            return HttpResponse(response)

    @abstractmethod
    def get(self, request, string_id):
        pass

    @abstractmethod
    def post(self, request, string_id):
        pass

    @abstractmethod
    def put(self, request, string_id):
        pass

    @abstractmethod
    def delete(self, request, string_id):
        pass
