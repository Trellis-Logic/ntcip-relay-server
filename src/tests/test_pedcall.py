from unittest import TestCase
from unittest.mock import MagicMock, patch
from ntcip_relay_server.module import pedcall
from uuid import UUID, uuid4


@patch("ntcip_relay_server.module.pedcall.Session")
class TestPedcallCallbacks(TestCase):
    def setUp(self) -> None:
        self.test_mib = "1.3.6.1.4.1.1206.4.2.1.1.5.1.7"
        self.test_phase_control_group = 1
        self.test_phase = 4
        self.test_enable_true = True
        self.test_timeout_seconds = 0.01
        self.test_uuid = uuid4()
        self.test_callback_uid = pedcall.PedcallCallbacks.callback_uid(self.test_mib, self.test_phase_control_group, self.test_phase)

    def test_pedcall_set_with_timeout_of_0_does_not_generate_callback(self, mock_session):
        pedcall.PedcallCallbacks._generate_callback = MagicMock()
        pedcall.pedcall_set(
            self.test_mib,
            self.test_phase_control_group,
            self.test_phase,
            self.test_enable_true,
            0
        )
        pedcall.PedcallCallbacks._generate_callback.assert_not_called()

    def test_pedcall_set_with_nonzero_timeout_generates_callback(self, mock_session):
        pedcall.PedcallCallbacks._generate_callback = MagicMock()
        pedcall.pedcall_set(
            self.test_mib,
            self.test_phase_control_group,
            self.test_phase,
            self.test_enable_true,
            self.test_timeout_seconds
        )
        pedcall.PedcallCallbacks._generate_callback.assert_called_once_with(
            self.test_mib,
            self.test_phase_control_group,
            self.test_phase,
            not self.test_enable_true,
            self.test_timeout_seconds
        )

    def test_pedcall_set_with_timeout_of_0_clears_an_existing_callback_and_does_not_generate_callback(self, mock_session):
        pedcall.pedcall_set(
            self.test_mib,
            self.test_phase_control_group,
            self.test_phase,
            self.test_enable_true,
            10
        )
        pedcall.PedcallCallbacks._generate_callback = MagicMock()
        pedcall.PedcallCallbacks._clear_callback = MagicMock()
        pedcall.pedcall_set(
            self.test_mib,
            self.test_phase_control_group,
            self.test_phase,
            self.test_enable_true,
            0
        )
        pedcall.PedcallCallbacks._clear_callback.assert_called_once_with(self.test_mib, self.test_phase_control_group, self.test_phase)
        pedcall.PedcallCallbacks._generate_callback.assert_not_called()

    def test_pedcall_set_with_nonzero_timeout_clears_existing_callback_and_generates_callback(self, mock_session):
        pedcall.pedcall_set(
            self.test_mib,
            self.test_phase_control_group,
            self.test_phase,
            self.test_enable_true,
            10
        )
        pedcall.PedcallCallbacks._generate_callback = MagicMock()
        pedcall.PedcallCallbacks._clear_callback = MagicMock()
        pedcall.pedcall_set(
            self.test_mib,
            self.test_phase_control_group,
            self.test_phase,
            self.test_enable_true,
            self.test_timeout_seconds
        )
        pedcall.PedcallCallbacks._clear_callback.assert_called_once_with(self.test_mib, self.test_phase_control_group, self.test_phase)
        pedcall.PedcallCallbacks._generate_callback.assert_called_once_with(
            self.test_mib,
            self.test_phase_control_group,
            self.test_phase,
            not self.test_enable_true,
            self.test_timeout_seconds
        )

    def test_clear_callback_removes_existing_entry_from_callbacks_dictionary(self, mock_session):
        pedcall.PedcallCallbacks.CALLBACKS = {
            self.test_callback_uid: self.test_uuid,
            "123": 456
        }
        pedcall.PedcallCallbacks._clear_callback(self.test_mib, self.test_phase_control_group, self.test_phase)
        self.assertNotIn(self.test_mib, pedcall.PedcallCallbacks.CALLBACKS)

    def test_clear_callback_with_nonexisting_callback_does_nothing(self, mock_session):
        pedcall.PedcallCallbacks.CALLBACKS = {
            "123": 456
        }
        pedcall.PedcallCallbacks._clear_callback(self.test_mib, self.test_phase_control_group, self.test_phase)
        self.assertNotIn(self.test_mib, pedcall.PedcallCallbacks.CALLBACKS)

    def test_generate_callback_adds_entry_to_callbacks_dictionary_with_uuid(self, mock_session):
        pedcall.PedcallCallbacks._execute_callback = MagicMock()
        pedcall.PedcallCallbacks._generate_callback(
            self.test_mib,
            self.test_phase_control_group,
            self.test_phase,
            self.test_enable_true,
            self.test_timeout_seconds
        )
        self.assertIn(self.test_callback_uid, pedcall.PedcallCallbacks.CALLBACKS)
        self.assertIsInstance(pedcall.PedcallCallbacks.CALLBACKS[self.test_callback_uid], UUID)

    @patch("ntcip_relay_server.module.pedcall.update_pedcall")
    def test_execute_callback_calls_update_pedcall_when_uuid_is_in_callbacks(self, mock_update_pedcall, mock_session):
        pedcall.PedcallCallbacks.CALLBACKS = {
            self.test_callback_uid: self.test_uuid,
            "123": 456
        }
        pedcall.PedcallCallbacks._execute_callback(
            self.test_uuid,
            self.test_mib,
            self.test_phase_control_group,
            self.test_phase,
            self.test_enable_true,
            0
        )
        mock_update_pedcall.assert_called_once_with(
            mock_session(),
            self.test_mib,
            self.test_phase_control_group,
            self.test_phase,
            self.test_enable_true,
        )

    @patch("ntcip_relay_server.module.pedcall.update_pedcall")
    def test_execute_callback_does_not_call_update_pedcall_when_uuid_is_not_in_callbacks(self, mock_update_pedcall, mock_session):
        pedcall.PedcallCallbacks.CALLBACKS = {
            "123": 456
        }
        pedcall.PedcallCallbacks._execute_callback(
            self.test_uuid,
            self.test_mib,
            self.test_phase_control_group,
            self.test_phase,
            self.test_enable_true,
            0
        )
        mock_update_pedcall.assert_not_called()
