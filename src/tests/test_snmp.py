from unittest import TestCase
from ntcip_relay_server.module.snmp import Session
from time import sleep
from datetime import datetime
from threading import Thread


class TestSession(TestCase):
    def test_consecutive_sessions_created_successfully(self):
        s = Session()
        s.close()
        s = Session()
        s.close()

    def test_multiple_sessions_cannot_be_created_at_the_same_time(self):
        def close_session_after_half_second(session):
            sleep(.5)
            session.close()
        start_time = datetime.now()
        s = Session()
        Thread(target=close_session_after_half_second, args=[s]).start()
        s = Session()
        s.close()
        end_time = datetime.now()
        self.assertGreaterEqual((end_time - start_time).total_seconds(), .5)
