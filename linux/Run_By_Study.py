import os
import re
import main

# Function to process each file (replace with your actual function)
def run_by_study(file_paths):
    print(f"Processing {len(file_paths)} files:")
    for path in file_paths:
        print(path)
        bms = main.BrainMetastasisSegmentation(path)
        bms.run()

def collect_files(study_id, base_dir):
    """
    Collect paths of all files that belong to a specific study.
    :param study_id: The study identifier (e.g., 'Study_249')
    :param base_dir: The base directory where the MRI data is stored
    :return: List of file paths corresponding to the study
    """
    study_files = []

    for root, dirs, files in os.walk(base_dir):
        # Look for folders that match the study pattern 
        folder_name = os.path.basename(root)
        
        if re.match(rf"Study_{study_id}", folder_name):
            for file in files:
                file_path = os.path.join(root, file)
                study_files.append(file_path)

    return study_files

def main_script(study_id):
    
    base_dir = '/home/eliyams/Downloads/MRI_nifti_only_t1ce'
    
    # Collect all file paths for the specified study
    study_files = collect_files(study_id, base_dir)
    
    # Pass these file paths to the main function
    if study_files:
        run_by_study(study_files)
    else:
        print(f"No files found for study {study_id}")

if __name__ == "__main__":
    study_id_input = input("Enter the study ID (e.g., '249'):")
    # study_ids = ['249', '350', '1575', '2400', '2959', '2963', '5490', '5620', '7227', '7642', '7993', '8216', '8608', '9558', '10794', '11438', '12017', '12976', '13209', '13328', '13837', '13910', '15882', '16358', '16821', '17218', '17543', '17934', '18079', '18718', '19524', '21665', '21824', '21863', '23985', '24075', '25293', '27869', '28142', '29035', '29281', '29969', '30146', '30721', '30904', '30938', '31058', '31558', '33310', '33442', '33955', '35479', '35582', '36913', '37768', '38542', '39782', '39832', '40834', '40840', '41757', '42341', '42501', '42664', '43491', '44375', '44757', '45002', '45615', '46175', '46426', '48119', '48637', '48857', '49442', '50086', '50491', '50508', '50545', '50570', '51254', '51844', '52724', '53305', '54819', '55576', '55873', '56402', '56845', '56917', '57367', '57727', '58018', '58101', '58102', '58729', '59380', '59924', '59949', '60087', '61011', '61196', '61436', '61883', '62607', '62769', '63277', '63926', '64147', '65267', '65959', '66316', '66788', '67049', '67186', '67334', '67546', '68113', '68413', '69290', '71181', '71368', '71505', '72291', '72894', '74003', '74458', '74993', '75320', '75398', '77079', '77341', '78381', '80208', '81205', '81209', '81210', '81501', '82449', '82911', '83001', '83633', '83764', '84860', '85221', '85286', '85472', '85555', '85704', '86625', '86699', '87156', '87515', '89345', '89358', '90137', '90279', '92826', '93455', '94317', '94834', '94980', '95635', '96201', '96261', '96619', '97160', '97771', '98341', '98729', '99167' ]
    # print(f'Running on {len(study_ids)} patients')
    # for study_id_input in study_ids:
    main_script(study_id_input)
