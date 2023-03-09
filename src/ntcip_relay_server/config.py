from pathlib import Path
import json


DEFAULT_CONFIG_LOCATION = Path("/data/config/config.json")


class Config:
    NTCIP_CONTROLLER_IP = '127.0.0.1'
    NTCIP_CONTROLLER_PORT = 161
    NTCIP_COMMUNITY = 'administrator'
    NTCIP_VERSION = 1
    HTTP_SERVER_PORT = 8080


    @classmethod
    def load_config_file(cls, config_file_location: Path) -> None:
        """
        Update the class variables with the configuration data provided in the config file
        :param config_file_location: a json formatted file
        :type config_file_location:
        :return:
        :rtype:
        """
        with open(config_file_location) as fpt:
            data = json.load(fpt)
        cls.NTCIP_CONTROLLER_IP = data.get('ntcip_controller_ip', cls.NTCIP_CONTROLLER_IP)
        cls.NTCIP_CONTROLLER_PORT = data.get('ntcip_controller_port', cls.NTCIP_CONTROLLER_PORT)
        cls.NTCIP_COMMUNITY = data.get('ntcip_community', cls.NTCIP_COMMUNITY)
        cls.NTCIP_VERSION = data.get('ntcip_version', cls.NTCIP_VERSION)
        cls.HTTP_SERVER_PORT = data.get('http_server_port', cls.HTTP_SERVER_PORT)

    @classmethod
    def to_json(cls) -> str:
        """
        Converts the current class variables to a JSON string; useful for creating a sample config file
        :return:
        :rtype:
        """
        config = {
            "ntcip_controller_ip": cls.NTCIP_CONTROLLER_IP,
            "ntcip_controller_port": cls.NTCIP_CONTROLLER_PORT,
            "ntcip_community": cls.NTCIP_COMMUNITY,
            "ntcip_version": cls.NTCIP_VERSION,
            "http_server_port": cls.HTTP_SERVER_PORT
        }
        return json.dumps(config, indent=4)
