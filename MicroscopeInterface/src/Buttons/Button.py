import MicroscopeInterface.src.Settings as Settings
import time


class Button:
    def __init__(self, image, timeout, gui_interface):
        """
        Encapsulate Button functionality

        :param image: Path to button image
        :param timeout: How long does the button stay in 'clicked' state for (s)
        :param gui_interface: UI object, that the button is part of
        :return: None
        """
        self._path_to_image = image
        self._timeout = timeout  # Timeout in seconds
        self._gui_interface = gui_interface
        self._last_clicked = 0
        return

    def get_path(self):
        """
        Get absolute path to button image

        :return: Path to image location
        """
        return self._path_to_image

    def is_pressed(self):
        """
        Check if button has been pressed

        :return: Boolean
        """
        return time.time() < self._last_clicked + self._timeout

    def press(self):
        """
        Press the button with the mouse

        :return: None
        """
        if self.is_pressed():
            # Wait until button isn't pressed anymore
            time.sleep(self._timeout + self._last_clicked - time.time())

        # Jump mouse to position
        pos = self._gui_interface.locateCenterOnScreen(self._path_to_image)
        self._gui_interface.moveTo(pos[0], pos[1], Settings.MOVEMENT_LENGTH)
        self._gui_interface.click()

        self._last_clicked = time.time()
