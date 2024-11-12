# MRI Image Processing and Segmentation

This project encompasses a pipeline for processing and analyzing MRI images, including conversion, resampling, normalization, registration, skull stripping, and segmentation. The project also includes visualization and analysis of segmented results. The pipeline utilizes several tools and libraries, including NIfTI handling, image processing with ANTs, and segmentation with AuroraInferer.

## Project Structure

1. **Data Preparation**
   - `main_preprocess.py`: Handles the preprocessing pipeline of MRI images.
     - **Functions**:
       - `load_data(data_path)`: Loads NIfTI data and prepares the results directory.
       - `dicomtonifti(data_path, output_path)`: Converts DICOM files to NIfTI format.
       - `resample(data)`: Resamples NIfTI images to isotropic voxel sizes.
       - `co_regstrate(data, output_path)`: Registers the NIfTI image to a reference image using ANTs.
       - `normalize(data)`: Normalizes NIfTI image data to the range [0, 1].
       - `skull_stripp(data, output_path)`: Applies skull stripping to the MRI image using HD-BET.
       - `main_preprocess(data_path)`: Runs the full preprocessing pipeline.

2. **Segmentation and Analysis**
   - `analysis.py`: Performs segmentation, overlays, and analysis of metastases.
     - **Functions**:
       - `overlay_segmentation_on_image(origin_data, mask_data, output_path, alpha=0.1)`: Overlays segmentation mask on the MRI image and saves the result.
       - `find_met_labaled_mask(mask)`: Labels connected components in a binary mask.
       - `find_met_loc_vol(labeled_mask_arr, num_mets)`: Computes properties of labeled metastasis regions.
       - `present_mets(num_mets, mets_properties)`: Prints information about detected metastases.
       - `main_analysis(result_path)`: Performs the analysis pipeline including overlay, labeling, and presenting results.

## Installation

To set up the project environment, use the provided YAML file to create and activate the environment. Follow these steps:

1. **Create and activate the environment**:
   
   1. Ensure you have [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) installed. 
   2. Ensure you have the right Python version (3.11.9).
   3. cd your terminal into the project folder.
   4. Then, use the following command to create and activate the environment:

   ```bash
   conda env create -f environment.yml
   conda activate env_final_project
  Make sure to select interperter that support this env
  
## Run


**To run the pipeline:**
go to main.py and paste the path to your nifti file in the 'data_path' variable. Then use the following command(in the project folder):

 ```bash
python main.py
```


**To run by study id use the following command in the terminal:**

 ```bash
/home/eliyams/anaconda3/envs/env_final_project/bin/python /home/eliyams/Downloads/FinalProject-main/linux/Run_By_Study.py
```

Then you will recive a poping message "Enter the study ID (e.g., '249'):" after writing the study id press enter and the pipeline will start for all files in this study. 

All of the results can be found in the originial study directory under subdirectory "results". 



**To run count for all metastasis found in a list of scan:**


First create a list of file names you want to count in the following format: 
"filename", "filename2", "filename3" 

Open visual studio code and open the script found in:/home/eliyams/Downloads/FinalProject-main/linux/Count_Mets.py

Then paste your list in line 32 in the file like this: 
file_names = ["filename", "filename2", "filename3"]  

press Ctrl+S or file -> save

Press Ctrl+Alt+N or Run the following command:

```bash
/home/eliyams/anaconda3/envs/env_final_project/bin/python /home/eliyams/Downloads/FinalProject-main/linux/Count_Mets.py
```

The count will be printed in the terminal section.
