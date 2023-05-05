import os
import shutil
import urllib.request
import zipfile

# Define the URL of the Git repository containing your program.
repo_url = 'https://github.com/treehuggersystems/stacklight.git'

# Define the name of the folder where the program's files will be extracted.
folder_name = 'stacklight'

# Define the name of the config file and icon file you want to create.
config_file_name = 'config.txt'
icon_file_name = 'stacklight.ico'

# Define the paths to the startup folder and the current user folder.
startup_folder_path = os.path.join(os.environ['APPDATA'], 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
current_user_folder_path = os.path.join(os.path.expanduser("~"),'.TeamsStatus')

# Clone the Git repository to a temporary directory.
temp_dir = os.path.join(os.path.dirname(__file__), 'temp')
shutil.rmtree(temp_dir, ignore_errors=True)
os.makedirs(temp_dir)
os.system(f'git clone {repo_url} {temp_dir}')

# Extract the program's files from the Git repository to the startup folder.
folder_path = os.path.join(temp_dir, folder_name)
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    if os.path.isfile(filepath) and os.path.splitext(filename)[1] in ('.exe', '.bat', '.cmd'):
        shutil.copy(filepath, startup_folder_path)

# Create the config file and icon file in the current user folder.
config_file_path = os.path.join(current_user_folder_path, config_file_name)
icon_file_path = os.path.join(current_user_folder_path, icon_file_name)
with open(config_file_path, 'w') as config_file:
    config_file.write('This is the config file for your program.')
urllib.request.urlretrieve('https://www.example.com/icon.ico', icon_file_path)

# Clean up the temporary directory.
shutil.rmtree(temp_dir)
