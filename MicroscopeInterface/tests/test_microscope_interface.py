import pytest
from MicroscopeInterface.src import LeicaMicroscope, LeicaUI
from MicroscopeInterface.src.Buttons import CaptureImage, ForwardsButton, BackwardsButton, LeftButton, RightButton, \
    MakeLive, AcquisitionTab, ExperimentsTab, SeqButton, StartButton, SaveButton


class TestMicroscopeInterface(object):

    @pytest.fixture
    def universe(self, mocker):

        ci = CaptureImage.CaptureImage('NO_IMAGE', mocker.Mock())
        fb = ForwardsButton.ForwardsButton('NO_IMAGE', mocker.Mock())
        bb = BackwardsButton.BackwardsButton('NO_IMAGE', mocker.Mock())
        lb = LeftButton.LeftButton('NO_IMAGE', mocker.Mock())
        rb = RightButton.RightButton('NO_IMAGE', mocker.Mock())
        ml = MakeLive.MakeLive('NO_IMAGE', mocker.Mock())
        aq = AcquisitionTab.AcquisitionTab('NO_IMAGE', mocker.Mock())
        ex = ExperimentsTab.ExperimentsTab('NO_IMAGE', mocker.Mock())
        se = SeqButton.SeqButton('NO_IMAGE', mocker.Mock())
        st = StartButton.StartButton('NO_IMAGE', mocker.Mock())
        sv = SaveButton.SaveButton('NO_IMAGE', mocker.Mock())

        ci.press = mocker.stub(name='press')
        fb.press = mocker.stub(name='press')
        bb.press = mocker.stub(name='press')
        lb.press = mocker.stub(name='press')
        rb.press = mocker.stub(name='press')
        ml.press = mocker.stub(name='press')
        aq.press = mocker.stub(name='press')
        ex.press = mocker.stub(name='press')
        se.press = mocker.stub(name='press')
        st.press = mocker.stub(name='press')
        sv.press = mocker.stub(name='press')

        ui = LeicaUI.LeicaUI(forwards_button=fb, backwards_button=bb, left_button=lb, right_button=rb, capture_image=ci,
                             make_live=ml, acquisition_tab=aq, experiments_tab=ex, seq_button=se, start_button=st, save_button=sv)
        ms = LeicaMicroscope.LeicaMicroscope(ui, "TEST_EXPERIMENT_LOCATION")

        return {"fb": fb, "lb": lb, "rb": rb, "bb": bb, "ci": ci, "ml": ml, "aq": aq, "ex": ex, "se": se, "st": st,
                "ui": ui, "ms": ms, "sv": sv}

    def test_press_capture_image_button(self, universe):
        universe['ms'].take_picture()
        universe['aq'].press.assert_called_once_with()
        universe['se'].press.assert_called_once_with()
        universe['st'].press.assert_called_once_with()
        universe['ex'].press.assert_called_once_with()


    def test_move_right(self, universe):
        universe['ms'].move_right()
        assert universe['rb'].press.call_count == universe['ms'].X_MOVE_STEP

    def test_move_left(self, universe):
        universe['ms'].move_left()
        assert universe['lb'].press.call_count == universe['ms'].X_MOVE_STEP

    def test_move_forwards(self, universe):
        universe['ms'].move_forwards()
        assert universe['fb'].press.call_count == universe['ms'].Y_MOVE_STEP

    def test_move_backwards(self, universe):
        universe['ms'].move_backwards()
        assert universe['bb'].press.call_count == universe['ms'].Y_MOVE_STEP

