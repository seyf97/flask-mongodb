from typing import Mapping, Any
from flask import Response
from bson import json_util


def bson_to_json(bson: Mapping[str, Any]) -> Response:
    return Response(
        json_util.dumps(bson),
        content_type="application/json",
    )