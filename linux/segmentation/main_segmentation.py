from brainles_aurora.inferer import AuroraInferer, AuroraInfererConfig
import os

def segment(result_path):
    """
    Performs image segmentation using the AuroraInferer.

    This function sets up the configuration for the AuroraInferer, creates an instance of it, 
    and runs inference on the specified T1-weighted MRI image. The results are saved to 
    the specified paths for segmentation and metastasis mask.

    Parameters:
    - data_path (str): Path to the directory containing the preprocessed NIfTI image.

    The function assumes the "preprocess.nii" file (the preprocessed T1-weighted MRI image) 
    exists in the `data_path` directory.

    This function will create the following files in the `data_path` directory:
    - "segmentation.nii": A 3D binary mask of the entire brain abnormalities, including metastases and edema.
    - "mask.nii": A 3D binary mask specifically for metastases.

    Returns:
    - None: This function does not return any value. The results are saved to files.
    """
    t1c_path = os.path.join(result_path,"preprocess.nii")
    segmentation_path = os.path.join(result_path,"segmentation.nii")
    metastasis_mask_path = os.path.join(result_path,"mask.nii")

    config = AuroraInfererConfig(
        tta=False,
        sliding_window_batch_size=4,
        cuda_devices="0",  
        # device="cpu",
    )

    inferer = AuroraInferer(config=config)

    _ = inferer.infer(
        t1c = t1c_path,
        segmentation_file = segmentation_path,
        metastasis_unbinarized_floats_file = metastasis_mask_path
    )
# path = 'DICOM files/7227/MRI T1 contrast enhanced/07227_MRI T1CE_15102021/Results'
# f = segment(path)
       