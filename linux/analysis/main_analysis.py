import nibabel as nib
from scipy import ndimage
import matplotlib.pyplot as plt
import os
import numpy as np

def overlay_segmentation_on_image(origin_data, mask_data, result_path, alpha=0.1):
    """
    Overlays a binary mask onto an MRI image and saves the result as a NIfTI file.

    This function creates a color overlay of the mask on top of the original MRI image. 
    The mask is colored red and blended with the original image based on the specified alpha value.

    Parameters:
    - origin_data (nib.Nifti1Image): The original MRI image.
    - mask_data (nib.Nifti1Image): The binary mask image.
    - result_path (str): Directory where the output overlay image will be saved.
    - alpha (float): Blending factor for the overlay (default is 0.1). A higher value makes the mask more prominent.

    Returns:
    - None: The function does not return any value. The result is saved to a file.
    """
    origin = origin_data.get_fdata()
    mask = mask_data.get_fdata()

    mask_color = np.array([255, 0, 0])
    origin_rgb = np.stack([origin]*3, axis=-1)
    origin_rgb = origin_rgb / np.max(origin_rgb)
    
    mask_rgb = np.zeros_like(origin_rgb)
    mask_rgb[mask != 0] = mask_color
    overlay = (1 - alpha) * origin_rgb + alpha * (mask_rgb / 255)
    
    overlay_rgb = (overlay * 255).astype(np.uint8)
    
    shape_3d = overlay_rgb.shape[:3]
    rgb_dtype = np.dtype([('R', 'u1'), ('G', 'u1'), ('B', 'u1')])
    overlay_rgb = overlay_rgb.copy().view(dtype=rgb_dtype).reshape(shape_3d)
    
    ni_img = nib.Nifti1Image(overlay_rgb, origin_data.affine)
    output_file = os.path.join(result_path, f"overlay.nii")
    nib.save(ni_img, output_file)
    print(f'Overlay saved as {output_file}')


def find_met_labaled_mask(mask):
    """
    Labels connected components in a binary mask.

    Parameters:
    - mask (numpy.ndarray): Binary mask where connected components will be labeled.

    Returns:
    - labeled_mask_arr (numpy.ndarray): Array with labeled connected components.
    - num_mets (int): Number of labeled components (metastases).
    """
    labeled_mask_arr, num_mets = ndimage.label(mask)
    return labeled_mask_arr, num_mets


def find_met_loc_vol(labeled_mask_arr, num_mets):
    """
    Computes properties of labeled metastasis regions.

    Parameters:
    - labeled_mask_arr (numpy.ndarray): Array with labeled connected components.
    - num_mets (int): Number of labeled components.

    Returns:
    - mets_properties (list of dict): List of dictionaries containing properties of each metastasis, 
      including label, volume, and center of mass.
    """
    mets_properties = []
    for label_idx in range(1, num_mets + 1):
        label_mask = (labeled_mask_arr == label_idx)
        
        volume = np.count_nonzero(label_mask)
        center_of_mass = ndimage.measurements.center_of_mass(label_mask)
        mets_properties.append({'label': label_idx, 'volume': volume, 'center_of_mass': center_of_mass})


    return mets_properties


def present_mets(num_mets, mets_properties):
    """
    Prints information about detected metastases.

    Parameters:
    - num_mets (int): Number of metastases detected.
    - mets_properties (list of dict): List of dictionaries with properties of each metastasis.
    
    Returns:
    - None: The function prints the results but does not return any value.
    """
    print(f'\nIn this MRI scan {num_mets} metastasis were found:\n')
    for met_props in mets_properties:
        label = met_props['label']
        volume = met_props['volume']
        center_of_mass = met_props['center_of_mass']
        print(f"Label: {label}, Volume: {volume}[mm^3], Center of Mass (approximate): {center_of_mass}\n")


def main_analysis(result_path):
    processed_path = os.path.join(result_path,"preprocess.nii")
    origin = nib.load(processed_path)

    metastasis_mask_path = os.path.join(result_path,"mask.nii")
    mask = nib.load(metastasis_mask_path)

    overlay_segmentation_on_image(origin, mask, result_path)

    mask = mask.get_fdata()
    labeled_mask_arr, num_mets = find_met_labaled_mask(mask)
    mets_properties = find_met_loc_vol(labeled_mask_arr, num_mets)
    properties_path = os.path.join(result_path,"properties.txt")
    with open(properties_path, 'w') as file:
        file.write(str(mets_properties))
    present_mets(num_mets, mets_properties)
