"""
Setup configuration for PyTestSuite Pro

This file enables installation of the framework as a package
and defines project metadata and dependencies.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = []
requirements_file = this_directory / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="pytestsuite-pro",
    version="1.0.0",
    author="PyTestSuite Pro Team",
    author_email="contact@pytestsuite-pro.com",
    description="Advanced Hybrid Test Automation Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/PyTestSuite-Pro",
    project_urls={
        "Bug Tracker": "https://github.com/your-org/PyTestSuite-Pro/issues",
        "Documentation": "https://github.com/your-org/PyTestSuite-Pro#readme",
        "Source Code": "https://github.com/your-org/PyTestSuite-Pro",
    },
    
    packages=find_packages(),
    
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Software Development :: Quality Assurance",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Framework :: Pytest",
    ],
    
    python_requires=">=3.8",
    
    install_requires=requirements,
    
    extras_require={
        "dev": [
            "black>=23.0.0",
            "flake8>=6.0.0", 
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "allure": [
            "allure-pytest>=2.13.0",
        ],
        "excel": [
            "openpyxl>=3.1.0",
        ],
    },
    
    entry_points={
        "console_scripts": [
            "pytestsuite-pro=core.cli:main",
        ],
        "pytest11": [
            # "pytestsuite_pro = conftest",
        ]
    },
    
    package_data={
        "": [
            "*.ini",
            "*.yaml", 
            "*.yml",
            "*.json",
            "*.csv",
            "test_data/**/*",
            "reports/.gitkeep",
        ]
    },
    
    include_package_data=True,
    
    keywords=[
        "pytest",
        "selenium", 
        "test automation",
        "testing framework",
        "ui testing",
        "api testing",
        "integration testing",
        "parallel testing",
        "page object model",
        "data driven testing",
        "keyword driven testing",
        "hybrid framework"
    ],
    
    zip_safe=False,
)