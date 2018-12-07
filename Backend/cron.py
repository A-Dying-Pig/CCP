from django.shortcuts import render
from .models import *
from django.http import JsonResponse, Http404, HttpResponse
from django.contrib.auth.decorators import login_required
import json
import time
import os
from .utils import *
import pytz
from datetime import datetime

def testCron():
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))