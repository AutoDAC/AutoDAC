import platform
import psutil
import subprocess
if platform.system() == 'Windows':
    from pywinauto.findwindows import find_window
    from pywinauto.win32functions import SetForegroundWindow


LASAF_process_name = "LASAFApplication.exe *32"
LASAF_executable_location = "D:\\Program Files(x86)\\Leica Microsystems CMS Cmb\\LAS AF\\BIN\\LASAFApplication.exe"


class LeicaUI:
    def __init__(self, forwards_button, backwards_button, left_button, right_button, capture_image, make_live,
                 acquisition_tab, experiments_tab, seq_button, start_button, save_button):
        """
        Interact with the LeicaUI

        :param forwards_button:     Button object, representing forwards
        :param backwards_button:    Button object, representing backwards
        :param left_button:         Button object, representing left
        :param right_button:        Button object, representing right
        :param capture_image:       Button object, representing capture image
        :param make_live:           Button object, representing go live
        :param acquisition_tab:     Button object, representing acqusition
        :param experiments_tab:     Button object, representing experiments
        :param seq_button:          Button object, representing seq
        :param start_button:        Button object, representing start
        :param save_button:         Button object, representing save
        :return: None
        """
        self._forwards_button = forwards_button
        self._backwards_button = backwards_button
        self._left_button = left_button
        self._right_button = right_button
        self._capture_image = capture_image
        self._make_live = make_live
        self._acquisition_tab = acquisition_tab
        self._experiments_tab = experiments_tab
        self._seq_button = seq_button
        self._start_button = start_button
        self._save_button = save_button

    def click_forwards_button(self):
        """
        Click up button

        :return: None
        """
        self._forwards_button.press()

    def click_backwards_button(self):
        """
        Click down button

        :return: None
        """
        self._backwards_button.press()

    def click_left_button(self):
        """
        Click left button

        :return: None
        """
        self._left_button.press()

    def click_right_button(self):
        """
        Click right button

        :return: None
        """
        self._right_button.press()

    def click_capture_image_button(self):
        """
        Click take image button

        :return: None
        """
        self._capture_image.press()

    def click_make_live_button(self):
        """
        Click make live button

        :return: None
        """
        self._make_live.press()

    def click_acquisition_tab(self):
        """
        Click acquisition tab

        :return: None
        """
        self._acquisition_tab.press()

    def click_experiments_tab(self):
        """
        Click experiments tab

        :return: None
        """
        self._experiments_tab.press()

    def click_seq_button(self):
        """
        Click seq button

        :return: None
        """
        self._seq_button.press()

    def click_start_button(self):
        """
        Click start button

        :return: None
        """
        self._start_button.press()

    def click_save_button(self):
        """
        Click save button

        :return: None
        """
        self._save_button.press()
