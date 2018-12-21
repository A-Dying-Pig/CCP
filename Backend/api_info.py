from django.http import JsonResponse, Http404, HttpResponse

def about(request):
    title = "CCP团队"
    content = "CCP团队在这里给大家拜年了！"
    return JsonResponse({'title': title, 'content': content})
