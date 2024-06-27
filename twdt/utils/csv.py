import csv
from typing import Any, Iterable, NoReturn, TextIO


class CSV(csv.DictReader):

    def __init__(self,
        f: TextIO,
        *args: Any,
        template: str | TextIO | None = None,
        required_headers: Iterable[str] | None = None,
        **kwargs: Any,
    ) -> None:

        super().__init__(f, *args, **kwargs)

        if template or required_headers:
            self.csv_check(f, template, required_headers, **kwargs)

    def csv_check(self,
        f: TextIO,
        template: str | TextIO | None = None,
        required_headers: Iterable[str] | None = None,
        **kwargs: Any,
    ) -> NoReturn:

        check_headers: set[str] = self.csv_get_headers(template, required_headers)
        data_headers: set[str] = set(self.fieldnames)
        missing_headers: str = ", ".join(list(check_headers - data_headers))

        if missing_headers:
            raise Exception(f"Missing headers: {missing_headers}")

    def csv_get_headers(self,
        template: str | TextIO | None = None,
        required_headers: Iterable[str] | None = None,
    ) -> set[str]:

        if required_headers:
            return set(required_headers)

        if not template:
            raise Exception("Template argument is required")

        if isinstance(template, str):
            with open(template) as fp:
                return set(csv.DictReader(fp).fieldnames)

        return set(csv.DictReader(template).fieldnames)
