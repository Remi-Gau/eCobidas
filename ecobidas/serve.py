#!/usr/bin/env python3

# https://stackoverflow.com/a/21957017

import os
from http.server import HTTPServer, SimpleHTTPRequestHandler, test
from pathlib import Path

from loguru import logger


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self) -> None:
        self.send_header("Access-Control-Allow-Origin", "*")
        SimpleHTTPRequestHandler.end_headers(self)


def serve(folder: str | Path | None = None) -> None:
    if folder is None or not Path(folder).exists():
        folder = (Path(__file__).parent / ".." / "cobidas_schema" / "schemas").absolute()

    logger.info(f"serving {folder}")

    os.chdir(folder)

    test(
        CORSRequestHandler,
        HTTPServer,
        port=8000,
    )


if __name__ == "__main__":
    serve()
