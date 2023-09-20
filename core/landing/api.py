from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.http import HttpRequest, JsonResponse
from rest_framework.parsers import JSONParser
import requests


@csrf_exempt
@require_http_methods(["POST"])
def send_request_api_view(request: HttpRequest) -> JsonResponse:
    tel = request.POST["tel"]
    name = request.POST["name"]
    tariff_type = request.POST.get("tariff_type", "Не выбран")
    chat_id = 308961543
    text = f"""
<b>Новая заявка</b>
    
<b>Имя</b>
{name}
<b>Телефон</b>
{tel}
<b>Тариф</b>
{tariff_type}
"""
    requests.post(
        url=f"https://api.telegram.org/bot1961963116:AAGzIJNqUnTV9OJOW18wcNmyd4eheLtsx0c/sendMessage?chat_id=1053749474&text={text}&parse_mode=HTML"
    )
    requests.post(
        url=f"https://api.telegram.org/bot1961963116:AAGzIJNqUnTV9OJOW18wcNmyd4eheLtsx0c/sendMessage?chat_id={chat_id}&text={text}&parse_mode=HTML"
    )

    return JsonResponse({"ok": True})
