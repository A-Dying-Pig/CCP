from django.shortcuts import render
from django.http import StreamingHttpResponse
import io

def file_iterator(file_name):
    f = io.open(file_name, 'rb')
    c = f.read() 
    f.close()  
    return c

def download(request):

    the_file_name =  request.path
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Disposition']='attachment;filename="{0}"'.format(path.split('/')[-1])
    return response
