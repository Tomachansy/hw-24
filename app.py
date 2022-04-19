import json
import os
from flask import Flask, request, Response
from werkzeug.exceptions import BadRequest

from tools import build_query

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query", methods=['POST'])
def perform_query() -> Response:
    """
    Обработка данных по запросам
    :raises BadRequest: if request is False
    :raises BadRequest: if file is False
    """
    try:
        data = json.loads(request.data)
        cmd1 = data['cmd1']
        value1 = data['value1']
        cmd2 = data['cmd2']
        value2 = data['value2']
        file_name = data['file_name']
    except KeyError:
        raise BadRequest

    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        raise BadRequest(description=f'{file_name} was not found')

    with open(file_path) as f:
        res = build_query(f, cmd1, value1)
        result = build_query(res, cmd2, value2)
        content = '\n'.join(result)
        print(content)

    return app.response_class(content, content_type="text/plain")



