import pytest
import os
import tempfile
import filecmp
import shutil
from MicroscopeInterface.src.IdentifySTEM import *

class TestIdentifyStem(object):
    @pytest.fixture
    def microscope(self, mocker):
        mock_microscope = mocker.Mock()
        return mock_microscope

    def test_merge_z_stack(self, microscope):
        source_image_dir = os.getcwd() + '/MicroscopeInterface/tests/z-stack-images/'
        test_result_img = os.getcwd() + '/MicroscopeInterface/tests/z-stack-merged-image/merge.tif'

        # Copy images to temp working dir
        working_dir = tempfile.mkdtemp()
        copy_dir_files(source_image_dir, working_dir)
        # Setup microscope
        microscope.working_dir = working_dir
        microscope.rgb_images = []
        for d in os.listdir(working_dir):
            microscope.rgb_images.append(cv2.imread(working_dir + '/' + d))

        # merge images
        merged_image = merge_z_stack(microscope=microscope)

        assert (merged_image == cv2.imread(test_result_img)).all()

        # clean up tmp dir
        shutil.rmtree(working_dir)

    def test_find_brightest_green(self, microscope):
        source_image_dir = os.getcwd() + '/MicroscopeInterface/tests/z-stack-images/'
        test_result_img = os.getcwd() + '/MicroscopeInterface/tests/z-stack-images/image_processed_3output_series_5_Z0_C0_T0.tif'

        # Copy images to temp working dir
        working_dir = tempfile.mkdtemp()
        copy_dir_files(source_image_dir, working_dir)
        # Setup microscope
        microscope.working_dir = working_dir
        microscope.rgb_images = []
        for d in os.listdir(working_dir):
            microscope.rgb_images.append(cv2.imread(working_dir + '/' + d))

        width, height, _ = microscope.rgb_images[0].shape
        brightest_image = analyse_z_stack(microscope, (0, width, 0, height))

        assert (brightest_image == cv2.imread(test_result_img)).all()

        # clean up tmp dir
        shutil.rmtree(working_dir)


def copy_dir_files(src_dir, dest_dir):
    for file_name in os.listdir(src_dir):
        full_file_name = os.path.join(src_dir, file_name)
        if (os.path.isfile(full_file_name)):
            shutil.copy(full_file_name, dest_dir)

def same_files(dir1, dir2):
    return len(filecmp.dircmp(dir1, dir2).common_files)\
        == len(os.listdir(dir1)) == len(os.listdir(dir2))
