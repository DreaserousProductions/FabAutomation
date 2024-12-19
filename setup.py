import os
from setuptools import setup, find_packages
from setuptools.command.install import install

class PostInstallCommand(install):
    """Custom post-install command to update the .env file."""

    def run(self):
        # Run the standard install process
        install.run(self)
        
        # Add or modify the .env file
        env_file_path = os.path.join(os.getcwd(), ".env")
        user = os.getenv("USERNAME") or os.getenv("USER")
        
        # Update .env file
        if user:
            user_data_dir = f"C:/Users/{user}/AppData/Local/Google/Chrome/User Data"
            with open(env_file_path, "a") as env_file:
                env_file.write(f"\nUSER_DATA_DIR={user_data_dir}\n")
            print(f"Updated .env with USER_DATA_DIR: {user_data_dir}")
        else:
            print("Could not determine the user. .env file not updated.")

setup(
    name="Fab Automation",
    version="1.0.0",
    author="Dreaserous Productions",
    author_email="dreaserousproductions@gmail.com",
    description="A package for auto-uploading, editing and deleting models on the fab website.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DreaserousProductions/FabAutomation",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "pyqt5",
        "python-dotenv",
        "selenium_stealth"
    ],
    cmdclass={
        'install': PostInstallCommand,
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)