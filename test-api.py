#!/usr/bin/env python3
import argparse
import json
import requests
from pathlib import Path


def get_default_api_key() -> str | None:

    try:
        with open(Path(__file__).parent / "api_key.txt" ) as fp:
            return fp.readline().strip()
    except Exception:
        return ""


def is_valid_token(value: str) -> str:
    if not value:
        raise ValueError(f"Invalid API token: {value}")
    return value


def get_args() -> argparse.Namespace:
    default_api_key: str | None = get_default_api_key()
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("-t", "--token",
        default=default_api_key,
        type=is_valid_token,
    )
    return parser.parse_args()


def main() -> None:
    args: argparse.Namespace = get_args()
    print(args.token)
    response: requests.Response = requests.post(
        url=args.url,
        headers={
            "X-API-KEY": args.token,
        },
    )

    if not response.ok:
        return print(f"{response.status_code}: {response.reason}")

    print(
        json.dumps(
            json.loads(response.content.decode("utf8")),
            indent=4,
        )
    )


main()
