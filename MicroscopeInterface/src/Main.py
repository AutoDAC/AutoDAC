import numpy as np
from MicroscopeInterface.src.IdentifySTEM import setup_microscope, identify_stem

def start_analysis(lif_path, save_path):
    """
    Use .lif file at lif_path to analyse scan, and save result in save_path

    :param lif_path: Path to .lif file to analyse
    :param save_path: Path to save output of analysis
    :return: Cell scores
    """
    microscope = setup_microscope(lif_path, save_path)

    # Take images and identify stem cells
    score = identify_stem(microscope)

    return np.array(score)
