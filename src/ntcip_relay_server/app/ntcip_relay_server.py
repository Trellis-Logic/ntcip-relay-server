import logging

from flask import Flask
from ntcip_relay_server import endpoint
from ntcip_relay_server.config import DEFAULT_CONFIG_LOCATION, Config
import argparse
import logging

app = Flask(__name__)
app.register_blueprint(endpoint.pedcall_api, url_prefix="/pedcall")


def cmdline():
    """
    Run the server from the commandline
    :return:
    :rtype:
    """
    parser = argparse.ArgumentParser(description='HTTP to NTCIP Relay Server')
    parser.add_argument('-c', '--config_file', default=DEFAULT_CONFIG_LOCATION, type=str,
                        help='The configuration file')
    parser.add_argument('-d', '--debug', action='store_true',
                        help='Enable debug logging')

    args = parser.parse_args()

    Config.load_config_file(args.config_file)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    app.run(host='0.0.0.0', port=Config.HTTP_SERVER_PORT, debug=args.debug)


