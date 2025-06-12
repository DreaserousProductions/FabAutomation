import subprocess

# Path to the file containing the list of packages
file_path = 'modules.txt'

# Read the list of modules from the file
with open(file_path, 'r') as file:
    modules = file.readlines()

# Clean up the module names (remove leading/trailing whitespaces)
modules = [module.strip() for module in modules]

# Install each module using pip
for module in modules:
    try:
        print(f"Installing {module}...")
        subprocess.check_call([ 'pip', 'install', module ])
        print(f"{module} installed successfully!")
    except subprocess.CalledProcessError:
        print(f"Failed to install {module}.")