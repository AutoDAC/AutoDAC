from MicroscopeInterface.src.Buttons.Button import Button


class SeqButton(Button):

    def __init__(self, image, gui_interface):
        super().__init__(image, 0, gui_interface)
