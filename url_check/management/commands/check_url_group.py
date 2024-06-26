from time import sleep
from typing import Any, cast

import requests

from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandParser

from url_check.models import UrlGroup, UrlCheck, UrlCheckFailure


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("url_group")
        parser.add_argument("-V", "--verbose", action="store_true")
        parser.add_argument("-s", "--sleep", type=int, default=0)

    def check_url(self, url_check: UrlCheck, **options: Any) -> bool:
        url: str = url_check.url
        url = f"https://{url}" if "://" not in url else url

        try:
            response: requests.Response | None = requests.get(
                url,
                timeout=url_check.timeout,
            )
            response = cast(requests.Response, response)
            status: int = response.status_code
            err_msg: str = response.reason

        except Exception as exc:
            response = None
            status = 0
            err_msg = str(exc)
            print(err_msg)

        if status == 200:
            if options["verbose"]:
                self.stdout.write(
                    f"{self.style.SUCCESS(str(status))}: {url}"
                )
            return True

        self.stdout.write(
            f"{self.style.ERROR(str(status))}: {url}"
        )

        UrlCheckFailure.objects.create(
            url_check=url_check,
            remarks=err_msg,
            status_code=status,
        )

        self.notify(
            url=url,
            status=status,
            reason=err_msg,
            url_check=url_check,
        )

        return False

    def handle(self, *args: Any, **options: Any) -> None:
        name: str = options["url_group"]
        url_group: UrlGroup | None = UrlGroup.objects.filter(name=name).first()
        if not url_group:
            raise Exception(f"Invalid URL group: {name}")

        while True:
            for obj in url_group.urlcheck_set.all():
                self.check_url(obj, **options)

            if not (sleep_seconds := options["sleep"]): break
            self.stderr.write(f"Sleeping {sleep_seconds}s...")
            sleep(sleep_seconds)

    def notify(self,
            url: str,
            status: int,
            reason: str,
            url_check: UrlCheck,
        ) -> None:

        recipient_list: list[str] = list(url_check
            .urlchecknotification_set
                .values_list("email", flat=True)
        )

        if url_check.notification_group:
            recipient_list += list(url_check
                .notification_group
                .notification_set
                .values_list("email", flat=True)
            )

        send_mail(
            subject=f"Website Alert ({status}): {url}",
            from_email=None,
            recipient_list=recipient_list,
            fail_silently=False,
            message=f"{url} {reason}",
        )
