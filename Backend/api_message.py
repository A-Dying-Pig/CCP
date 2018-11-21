from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json

def getnew(request):
    num = NotificationUser.objects.filter(user_id=request.user.id, read=False).count()
    return JsonResponse({
        'num': num
    })

def getall(request):
    amount = 8
    data = json.loads(request.body.decode('utf-8'))
    try:
        page = int(data['pageNum'])
    except:
        page = 1
    count = NotificationUser.objects.filter(user_id=request.user.id).count()
    total_page_num = (count - 1) // amount + 1
    ntf = NotificationUser.objects.all()[(page-1)*amount, page*amount]
    array = []
    for n in ntf:
        d = {}
        d['messageId'] = n.id
        d['context'] = Notification.objects.get(id=n.id).title
        d['read'] = 1 if n.read else 0
        array.append(d)

    return JsonResponse({
        'current_page_num': page,
        'total_page_num': total_page_num,
        'array': array
    })

def detail(request):
    data = json.loads(request.body.decode('utf-8'))
    mId = data['messageId']
    ntf = Notification.objects.get(id=mId)
    return JsonResponse({
        'title': ntf.title,
        'content': ntf.context
    })

