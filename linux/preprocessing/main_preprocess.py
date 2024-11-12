import nibabel as nib
from nibabel.processing import resample_to_output
import dicom2nifti
import ants
import numpy as np
from pathlib import Path
from typing import Union
from brainles_hd_bet import run_hd_bet
import os

def load_data(data_path):
    """
    Loads NIfTI data from the specified path and creates a directory for results.

    Parameters:
    - data_path (str): Path to the NIfTI file.

    Returns:
    - output_path (str): Path to the directory where results will be saved.
    - data (nib.Nifti1Image): Loaded NIfTI image data.
    """
    data = nib.load(data_path)
    folder_path = os.path.dirname(data_path)
    output_path = os.path.join(folder_path, "Results")
    os.makedirs(output_path, exist_ok=True)
    return output_path, data

'''Dicom to nifti converstion is not supported at the moment'''

# def dicomtonifti(data_path, output_path):
#     nifti_path=os.path.join(output_path, f"15_tra_t1_mprage_navc.nii.gz")
#     dicom2nifti.convert_directory(data_path, output_path)
#     data = nib.load(nifti_path)
#     return data

def resample(data):
    """
    Resamples the NIfTI image to have voxel sizes of 1 mm isotropic.

    Parameters:
    - data (nib.Nifti1Image): NIfTI image data to be resampled.

    Returns:
    - resampled_data (nib.Nifti1Image): Resampled NIfTI image data.
    """
    voxel_sizes = data.header.get_zooms()
    resampling_factor = (1.0 / voxel_sizes[0], 1.0 / voxel_sizes[1], 1.0 / voxel_sizes[2])
    resampled_data = resample_to_output(data, voxel_sizes=resampling_factor)
    return resampled_data

def co_regstrate(data, output_path):
    """
    Registers the NIfTI image to a fixed reference image using ANTs.

    Parameters:
    - data (nib.Nifti1Image): NIfTI image data to be registered.
    - output_path (str): Directory where temporary files will be saved.

    Returns:
    - registered_data (ants.ANTsImage): Registered NIfTI image data.
    """
    conver_path = os.path.join(output_path, f"temp_file.nii")
    nib.save(data, conver_path)
    data = ants.image_read(conver_path)
    os.remove(str(conver_path))

    refrence_data_path = 'linux/preprocessing/BraTS-GLI-01024-000-t1c.nii'
    fixed_image = ants.image_read(refrence_data_path)
    moving_image = data
    transform_type = "Rigid"

    registration_result = ants.registration(
        fixed=fixed_image,
        moving=moving_image,
        type_of_transform=transform_type,
    )

    registered_data = registration_result['warpedmovout']
    return registered_data

def normalize(data):
    """
    Normalizes the NIfTI image data to have values in the range [0, 1].

    Parameters:
    - data (nib.Nifti1Image): NIfTI image data to be normalized.

    Returns:
    - normalized_data (nib.Nifti1Image): Normalized NIfTI image data.
    """
    mri_data = data.get_fdata()  # Get the image data as a numpy array
    normalized_mri = (mri_data - np.min(mri_data)) / (np.max(mri_data) - np.min(mri_data))
    normalized_data = nib.Nifti1Image(normalized_mri, data.affine)
    return normalized_data

def skull_stripp(data, output_path):
    """
    Applies skull stripping to the NIfTI image using HD-BET.

    Parameters:
    - data (nib.Nifti1Image): NIfTI image data to be skull stripped.
    - output_path (str): Directory where the skull-stripped image will be saved.

    Returns:
    - data (nib.Nifti1Image): Skull-stripped NIfTI image data.
    """
    processed_path=os.path.join(output_path, f"temp_processed.nii.gz")
    nib.save(data, str(processed_path))
    
    def extract(
        input_image_path: str,
        masked_image_path: str,
        mode: str = "accurate",
        device: Union[int, str] = 0,
        do_tta: bool = True,
    ) -> None:
        """
        Skullstrips images with HD-BET and generates a skullstripped file and mask.

        Parameters:
        - input_image_path (str): Path to the input MRI image.
        - masked_image_path (str): Path where the skullstripped image will be saved.
        - mode (str): Mode for HD-BET (default is "accurate").
        - device (Union[int, str]): Device to run HD-BET on (default is 0).
        - do_tta (bool): Whether to use test-time augmentation (default is True).

        Returns:
        - None
        """
        run_hd_bet(
            mri_fnames=[input_image_path],
            output_fnames=[masked_image_path],
            mode=mode,
            device=device,
            postprocess=False,
            do_tta=do_tta,
            keep_mask=True,
            overwrite=True,
        )
    
    stripped_path=os.path.join(output_path, f"preprocess.nii")
    extract(
    input_image_path=processed_path,
    masked_image_path=stripped_path
    )

    data = nib.load(stripped_path)
    os.remove(str(processed_path))

    return data
        
def main_preprocess(data_path):
    print('\nPre-Process Started')
    output_path, data = load_data(data_path)
    print(f'\nResults can be found in {output_path}')
    # data = dicomtonifti(data_path, output_path)  
    data = resample(data)
    data = normalize(data)
    data = co_regstrate(data, output_path)
    data = skull_stripp(data, output_path)
    print('Pre-Process Completed')
    return output_path

# data_path = r'DICOM files/52724/MRI T1 contrast enhanced/52724_MRI T1CE_23062020/nifti/52.nii'
# output_path = r'FinalProject-main/DICOM files/52724/MRI T1 contrast enhanced/52724_MRI T1CE_23062020'
# base_path = Path(data_path)
# data = main_preprocess(base_path)

