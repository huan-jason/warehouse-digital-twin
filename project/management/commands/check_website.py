from typing import Any

from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandParser

import requests


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("urls", nargs="+", metavar="URL")
        parser.add_argument("-V", "--verbose", action="store_true")
        parser.add_argument("-r", "--recipients", metavar="recipients", nargs="*")

    def check_url(self, url: str, **options: Any) -> bool:
        if "://" not in url:
            url = f"https://{url}"

        response: requests.Response = requests.get(url)
        status: int = response.status_code

        if status != 200:
            self.stdout.write(
                f"{self.style.ERROR(str(status))}: {url}"
            )
            self.notify(
                url=url,
                status=status,
                response=response,
                **options,
            )

        elif options["verbose"]:
            self.stdout.write(
                f"{self.style.SUCCESS(str(status))}: {url}"
            )

        return status

    def handle(self, *args: Any, **options: Any) -> None:

        for url in options["urls"]:
            self.check_url(url, **options)

    def notify(self,
            url: str,
            status: int,
            response: requests.Response,
            **options: Any,
        ) -> None:

        if not (recipients := options["recipients"]):
            return

        send_mail(
            subject=f"Website Down ({status}): {url}",
            from_email=None,
            recipient_list=recipients,
            fail_silently=False,
            message=f"{url} {response.reason}",
        )