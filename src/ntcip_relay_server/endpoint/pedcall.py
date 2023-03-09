import json
from flask import Blueprint, request
from ntcip_relay_server.module import pedcall
import logging

pedcall_api = Blueprint("pedcall_api", __name__)


@pedcall_api.route('/', methods=['POST'])
def pedcall_endpoint():
    """

    :return:
    :rtype:
    """
    phase_control_group = int(request.form.get("phase_control_group"))
    phase = int(request.form.get("phase"))
    actuate = request.form.get("signal_type", False)
    if actuate == "true" or actuate == "True" or actuate == 1 or actuate == "1":
        actuate = True
    else:
        actuate = False
    logging.debug(f"actuate is {actuate}")
    mib = str(request.form.get("mib"))
    timeout_seconds = int(request.form.get("timeout_seconds", 0))
    result = {
        "state": pedcall.pedcall_set(mib, phase_control_group, phase, actuate, timeout_seconds)
    }

    return json.dumps(result), 200, {'ContentType': 'application/json'}

