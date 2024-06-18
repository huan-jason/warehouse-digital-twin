from functools import wraps
from typing import Any, Callable, Iterable, Optional

from django.http import HttpRequest, HttpResponse
from django.utils import timezone

from twdt.models import ApiKey


def api_key_check(f) -> Callable[..., HttpResponse]:

    @wraps(f)
    def wrapper(self, request:HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not check_api_key(request):
            return HttpResponse("Invalid API key", status=401)
        return f(self, request, *args, **kwargs)

    return wrapper


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


def remove_keys(data: dict[str, Any], addtional_keys: Iterable[str] | None = None) -> dict[str, Any]:
    include_keys: set[str] = {
        "location_id",
        "pallet_id",
    }
    exclude_keys: set[str] = {
        "warehouse",
        "rack",
        "rack_location",
    } | set(addtional_keys or {})

    return {
        key.replace("_", " "): val
        for key, val in data.items()
        if (not key.endswith("id") or key in include_keys)
            and key not in exclude_keys
    }
