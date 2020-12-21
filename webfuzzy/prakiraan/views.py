from django.http import HttpResponse
from django.template import loader
from .models import Cuaca


def index(request):
    dataCuaca = Cuaca.objects.order_by('id')[:20]
    template = loader.get_template('prakiraan/index.html')
    context = {
        'dataCuaca': dataCuaca,
    }
    return HttpResponse(template.render(context, request))