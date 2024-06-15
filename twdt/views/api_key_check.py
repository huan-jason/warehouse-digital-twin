from functools import wraps
from typing import Any, Callable, Optional

from django.http import HttpRequest, HttpResponse
from django.utils import timezone

from twdt.models import ApiKey


def check_api_key(request: HttpRequest) -> bool:
    if request.user.is_authenticated:
        return True

    api_key: Optional[str] = request.headers.get("X-API-KEY")
    if not api_key:
        return False

    obj: Optional[ApiKey] = ApiKey.objects.filter(api_key=api_key).first()
    if not obj:
        return False

    if obj.expiry < timezone.now():
        return False

    return True


def api_key_check(f) -> Callable[..., HttpResponse]:

    @wraps(f)
    def wrapper(self, request:HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not check_api_key(request):
            return HttpResponse("Invalid API key", status=418)

        return f(self, request, *args, **kwargs)

    return wrapper
