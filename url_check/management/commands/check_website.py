from typing import Any

from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandParser

import requests


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("urls", nargs="+", metavar="URL")
        parser.add_argument("-V", "--verbose", action="store_true")
        parser.add_argument("-r", "--recipients")

    def check_url(self, url: str, **options: Any) -> bool:
        if "://" not in url:
            url = f"https://{url}"

        response: requests.Response | None = None
        err_msg: str = ""

        try:
            response = requests.get(url, timeout=5)
            status: int = response.status_code

        except Exception as exc:
            err_msg = str(exc)
            print(err_msg)
            status = 0

        if status != 200:
            self.stdout.write(
                f"{self.style.ERROR(str(status))}: {url}"
            )
            self.notify(
                url=url,
                status=status,
                reason=response.reason if response else err_msg,
                **options,
            )

        elif options["verbose"]:
            self.stdout.write(
                f"{self.style.SUCCESS(str(status))}: {url}"
            )

        return status == 200

    def handle(self, *args: Any, **options: Any) -> None:

        for url in options["urls"]:
            self.check_url(url, **options)

    def notify(self,
            url: str,
            status: int,
            reason: str,
            **options: Any,
        ) -> None:

        if not (recipients := options["recipients"]):
            return

        recipient_list: list[str] = [
            recipient for item in recipients.split(",")
            if (recipient := item.strip())
        ]

        send_mail(
            subject=f"Website Alert ({status}): {url}",
            from_email=None,
            recipient_list=recipient_list,
            fail_silently=False,
            message=f"{url} {reason}",
        )
