import pytest
import time
from MicroscopeInterface.src.Buttons.Button import Button


class TestButton(object):

    @pytest.fixture
    def button_no_timeout(self, mocker):
        mock_gui_interface = mocker.Mock()
        mock_gui_interface.configure_mock(**{'locateCenterOnScreen.return_value': (0, 0)})
        return Button('NO_IMAGE', 0, mock_gui_interface)

    @pytest.fixture
    def button_5s_timeout(self, mocker):
        mock_gui_interface = mocker.Mock()
        mock_gui_interface.configure_mock(**{'locateCenterOnScreen.return_value': (0, 0)})
        return Button('NO_IMAGE', 5, mock_gui_interface)

    def test_button_no_timeout_is_pressed_instantly(self, button_no_timeout):
        assert not button_no_timeout.is_pressed()
        button_no_timeout.press()
        assert not button_no_timeout.is_pressed()

    def test_button_while_pressed_wait_to_press_again(self, button_5s_timeout):
        assert not button_5s_timeout.is_pressed()
        button_5s_timeout.press()
        assert button_5s_timeout.is_pressed()
        start_time = time.time()
        button_5s_timeout.press()
        end_time = time.time()
        assert end_time - start_time >= 5
        time.sleep(5)  # Wait for button to unpress
        assert not button_5s_timeout.is_pressed()
