import os
import glob
import yaml
import pandas as pd


def extract_info_from_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    # Extract project name and domain
    project_name = data.get('metadata').get('labels').get('project-name')
    domain = data.get('spec').get('name')
    return project_name, domain

def process_yaml_files(folder_path):
    project_list= []
    yaml_files = glob.glob(os.path.join(folder_path, '*.yaml'))
    for yaml_file in yaml_files:
        project_name, domain = extract_info_from_yaml(yaml_file)
        file = os.path.basename(yaml_file)
        project = file.replace('-alpha-phac-gc-ca.yaml','').replace('-data-donnes-phac-aspc-gc-ca.yaml','').replace('-alpha-phac-aspc-gc-ca.yaml','').replace('-beta-phac-aspc-gc-ca.yaml','').replace('-data-phac-gc-ca.yaml','').replace('.yaml','')
        project_list.append((file,project,project_name,domain))
    return project_list

def find_setters_yaml(folder_path):
    setters_files = []
    for root, dirs, files in os.walk(folder_path):
        if "setters.yaml" in files:
            setters_files.append(os.path.join(root, "setters.yaml"))
    return setters_files

def extract_owner_info_from_yaml(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    # Extract project name and domain
    project_name = data.get('data').get('project-vanity-name')
    owners = data.get('data').get('iam-owners')
    return project_name, owners

# Specify the folder containing the YAML files
folder_path = './phac-dns-main/dns-records/'

# Process the YAML files in the specified folder
project_list = process_yaml_files(folder_path)

# Specify the folder path
folder_path = './acm-core-main/DMIA-PHAC/'

# Find all 'setters.yaml' files
setters_yaml_files = find_setters_yaml(folder_path)

# Print the list of 'setters.yaml' files
if not setters_yaml_files:
    print("No 'setters.yaml' files found in the specified folder and its subfolders.")
    exit(-1)
    
# project_name, owners
yaml_data = []

print("Found 'setters.yaml' files")
for file in setters_yaml_files:
    yaml_data.append(extract_owner_info_from_yaml(file))

dns_projects_names = [x[1].replace('-','').replace('_','').replace('.','') for x in project_list]
acm_core_project_names = [x[0].replace('-','').replace('_','').replace('.','') for x in yaml_data]

combined_data = []
for i in range (len(dns_projects_names)):
    for j in range (len(acm_core_project_names)):
        if(acm_core_project_names[j] in dns_projects_names[i] or dns_projects_names[i] in acm_core_project_names[j]):
            combined_data.append(project_list[i]+yaml_data[j])

df = pd.DataFrame(combined_data, columns=['DNSfile','project_name_extracted_from_filename','project_name','domain','project_name_in_acm_core','owners'])

df.to_csv('output.csv', index=False)