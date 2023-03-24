import json
from flask import Blueprint, request
from ntcip_relay_server.module import pedcall
import logging

pedcall_api = Blueprint("pedcall_api", __name__)


@pedcall_api.route('/', methods=['POST'])
def pedcall_endpoint():
    data = request.get_json()
    logging.info(f"Issuing pedcall endpoint with {data}")
    result = {
        "state": pedcall.pedcall_set(
            data.get('mib',None),
            data.get('phase_control_group', 1),
            data.get('phase',1),
            data.get('activate', False),
            data.get('timeout_seconds', 0)
        )
    }


    return json.dumps(result), 200, {'ContentType': 'application/json'}

