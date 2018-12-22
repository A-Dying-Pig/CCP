from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json
import traceback

def getnew(request):
    try:
        num = NotificationUser.objects.filter(user_id=request.user.id, read=False).count()
        return JsonResponse({
            'num': num,
            'msg': ''
        })
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误！'})

def getall(request):
    try:
        amount = 8
        data = json.loads(request.body.decode('utf-8'))
        try:
            page = int(data['pageNum'])
        except:
            page = 1
        count = NotificationUser.objects.filter(user_id=request.user.id).count()
        total_page_num = (count - 1) // amount + 1
        ntf = NotificationUser.objects.all()[(page-1)*amount: page*amount]
        array = []
        for n in ntf:
            d = {}
            print(n.notification_id)
            d['messageId'] = n.notification_id
            d['context'] = Notification.objects.get(id=n.notification_id).title
            d['read'] = 1 if n.read else 0
            array.append(d)

        return JsonResponse({
            'current_page_num': page,
            'total_page_num': total_page_num,
            'array': array,
            'msg': ''
        })
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误！'})

def detail(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        mId = data['messageId']
        try:
            ntf = Notification.objects.get(id=mId)
            return JsonResponse({
                'title': ntf.title,
                'content': ntf.context,
                'msg': ''
            })
        except:
            return JsonResponse({'msg': '您查找的消息不存在！'})
    except:
        traceback.print_exc()
        return JsonResponse({'msg': '未知错误！'})


