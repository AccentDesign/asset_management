import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views.generic import ListView
from django.views.generic.base import View

from assets.models import File
from authentication.views.mixins import ActivatedTeamRequiredMixin


class FileList(ActivatedTeamRequiredMixin, ListView):
    model = File


class FileUpload(ActivatedTeamRequiredMixin, View):

    def render_json_response(self, context_dict, status=200):
        json_context = json.dumps(context_dict, cls=DjangoJSONEncoder).encode('utf-8')
        return HttpResponse(json_context, content_type='application/json', status=status)

    def post(self, request, *args, **kwargs):
        file = File.objects.create(file=request.FILES['file'])
        response_dict = {
            'name': str(file),
            'url': file.file.url,
            'size': file.file.size
        }
        return self.render_json_response(response_dict, status=200)
