import easysnmp
from ntcip_relay_server.config import Config
from threading import Lock


class Session:
    SESSION_LOCK = Lock()

    def __init__(self):
        self.SESSION_LOCK.acquire()
        self.snmp_session = easysnmp.Session(
            hostname=Config.NTCIP_CONTROLLER_IP,
            remote_port=Config.NTCIP_CONTROLLER_PORT,
            community=Config.NTCIP_COMMUNITY,
            version=Config.NTCIP_VERSION
        )

    def close(self):
        del self.snmp_session
        self.SESSION_LOCK.release()

