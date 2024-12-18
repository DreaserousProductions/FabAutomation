import os
import sys
from setuptools import setup, find_packages

setup(
    name="Fab Automation",
    version="1.0.0",
    author="Dreaserous Productions",
    author_email="dreaserousproductions@gmail.com",
    description="A package for auto-uploading, editing and deleting models on the fab website.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/DreaserousProductions/your-repo-name",
    packages=find_packages(),
    install_requires=[
        "selenium",
        "pyqt5",
        "python-dotenv"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)


USER_DATA_DIR = f"C:/Users/{user}/AppData/Local/Google/Chrome/User Data"