# Create your views here.
from django.shortcuts import render_to_response
from fluorescence_fit.models import DataInput


def data_inputs(request):
    return render_to_response('data_inputs.html',
            {'data_inputs': DataInput.objects.all() })


