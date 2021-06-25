import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import filesizeformat
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import View

from assets.models import Asset, AssetFile
from authentication.views.mixins import ActivatedCollectionRequiredMixin


class AssetFileUpload(ActivatedCollectionRequiredMixin, View):

    def render_json_response(self, context_dict, status=200):
        json_context = json.dumps(context_dict, cls=DjangoJSONEncoder).encode('utf-8')
        return HttpResponse(json_context, content_type='application/json', status=status)

    @csrf_exempt
    def post(self, request, *args, **kwargs):
        asset = get_object_or_404(Asset, pk=kwargs.get('asset_pk'))
        file = AssetFile.objects.create(file=request.FILES['file'], asset=asset)
        response_dict = {
            'name': file.filename(),
            'url': file.fileurl(),
            'size': filesizeformat(file.filesize())
        }
        return self.render_json_response(response_dict, status=200)
