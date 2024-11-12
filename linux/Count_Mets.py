import os
import ast

def sum_labels_from_files(file_names, base_path):
    total_sum = 0
    
    for file_name in file_names:
        # Construct the path to the properties.txt file
        file_path = os.path.join(base_path, file_name, 'Results', 'properties.txt')
        
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                # Convert string representation of list to actual list of dictionaries
                data = ast.literal_eval(content)
                
                # Sum the labels in this file
                file_sum = sum(item['label'] for item in data)
                total_sum += file_sum
                print(f"Sum for {file_name}: {file_sum}")
        
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
    
    return total_sum

# Example usage:
base_path = '/home/eliyams/Downloads/MRI_nifti_only_t1ce'

file_names = ["Study_249_2019-11-26", "Study_249_2019-09-15"]  
# file_names = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f))]

total_label_sum = sum_labels_from_files(file_names, base_path)
print(f"Total sum of all metastasis: {total_label_sum}")
