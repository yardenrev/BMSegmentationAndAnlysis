from preprocessing import main_preprocess
from segmentation import main_segmentation
from analysis import main_analysis
from pathlib import Path

class BrainMetastasisSegmentation:
    def __init__(self, nifti_path):
        self.data_path = nifti_path
    
    def preprocess(self):
        result_path = main_preprocess.main_preprocess(self.data_path)
        self.result_path = result_path
    
    def segment(self):
        main_segmentation.segment(self.result_path)

    def analyze(self):
        main_analysis.main_analysis(self.result_path)
    
    def run(self):
        self.preprocess()
        self.segment()
        self.analyze()

if __name__ == "__main__":
    data_path = r'DICOM files/52724/MRI T1 contrast enhanced/52724_MRI T1CE_23062020/nifti/52.nii'
    bms = BrainMetastasisSegmentation(data_path)
    bms.run()

