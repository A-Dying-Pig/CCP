from django.shortcuts import render
from django.http import FileResponse
import io
from os import path
from Backend.utils import RESOURCE_BASE_DIR

def download(request):
    # todo privilleges
    the_file_name = RESOURCE_BASE_DIR + request.path
    f = open(the_file_name, 'rb')
    response = FileResponse(f)
    response['Content-Disposition']='attachment;filename="{0}"'.format(path.split('/')[-1])
    return response
