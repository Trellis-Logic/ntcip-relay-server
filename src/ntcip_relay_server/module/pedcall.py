import logging
from .snmp import Session
from threading import Thread
from uuid import uuid4
from time import sleep
from easysnmp import EasySNMPError


class PedcallCallbacks:
    """
    Pedcall callback race conditions are implicitly handled by the session lock
    """

    @staticmethod
    def callback_uid(mib, phase_control_group, phase):
        return f"{mib}.{phase_control_group}.{phase}"

    CALLBACKS = {}

    @classmethod
    def update_callback(cls, mib, phase_control_group, phase, enable_true, timeout_seconds, session):
        """

        :param mib:
        :type mib:
        :param phase_control_group:
        :type phase_control_group:
        :param phase:
        :type phase:
        :param enable_true:
        :type enable_true:
        :param timeout_seconds:
        :type timeout_seconds:
        :param session: Not actually used, but needed to hold the session lock
        :type session:
        :return:
        :rtype:
        """
        cls._clear_callback(mib, phase_control_group, phase)
        if timeout_seconds:
            cls._generate_callback(mib, phase_control_group, phase, enable_true, timeout_seconds)

    @classmethod
    def _clear_callback(cls, mib, phase_control_group, phase):
        uid = cls.callback_uid(mib, phase_control_group, phase)
        if uid in cls.CALLBACKS:
            del cls.CALLBACKS[uid]

    @classmethod
    def _generate_callback(cls, mib, phase_control_group, phase, enable_true, timeout_seconds):
        uuid = uuid4()
        uid = cls.callback_uid(mib, phase_control_group, phase)
        cls.CALLBACKS[uid] = uuid
        Thread(target=PedcallCallbacks._execute_callback, args=[uuid, mib, phase_control_group, phase, enable_true, timeout_seconds]).start()

    @classmethod
    def _execute_callback(cls, uuid, mib, phase_control_group, phase, enable_true, timeout_seconds):
        sleep(timeout_seconds)
        session = Session()
        uid = cls.callback_uid(mib, phase_control_group, phase)
        if cls.CALLBACKS.get(uid, None) == uuid:
            try:
                update_pedcall(session, mib, phase_control_group, phase, enable_true)
            except EasySNMPError:
                logging.exception("SNMP Error in pedcall")
            except Exception:
                logging.exception("Unspecified error")
        session.close()

def get_pedcall_status(session, mib, phase_control_group):
    pedcall_phase_oid = f"{ mib }.{ phase_control_group }"
    description = session.get(pedcall_phase_oid)
    return int(description.value)

def set_pedcall_status(session, mib, phase_control_group, new_state):
    pedcall_phase_oid = f"{ mib }.{ phase_control_group }"
    description = session.set(pedcall_phase_oid, new_state, snmp_type="int")
    return description

def modify_phase(temp_state, phase, actuate_true):
    if actuate_true:
        new_state = temp_state | (1 << (phase-1))
    else:
        new_state = temp_state & ~(1 << (phase - 1))
    return new_state

def update_pedcall(session, mib, phase_control_group, phase, enable_true):
    value = get_pedcall_status(session.snmp_session, mib, phase_control_group)
    temp_state = value
    new_state = modify_phase(temp_state, phase, enable_true)
    set_pedcall_status(session.snmp_session, mib, phase_control_group, new_state)
    return get_pedcall_status(session.snmp_session, mib, phase_control_group)

def pedcall_set(mib, phase_control_group, phase, enable_true, timeout_seconds):
    session = Session()
    logging.debug(f"Request:"
                  f"mib: {mib} "
                  f"phase_control_group: {phase_control_group} "
                  f"phase: {phase} "
                  f"enable-true: {enable_true} "
                  f"timeout: {timeout_seconds} ")
    try:
        PedcallCallbacks.update_callback(mib, phase_control_group, phase, not enable_true, timeout_seconds, session)
        value = update_pedcall(session, mib, phase_control_group, phase, enable_true)
    except EasySNMPError:
        logging.exception("SNMP Error in pedcall")
    except Exception:
        logging.exception("Unspecified error")
    session.close()
    return value
