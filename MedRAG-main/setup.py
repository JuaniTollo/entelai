from setuptools import setup, find_packages

setup(
    name="MedRAG",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={"": ["templates/*.jinja", "data/*.py"]},  # Include template and data files
    install_requires=[
        'numpy',  # Example dependency, add others as needed
        'torch',
        'transformers'
    ],
    entry_points={
        'console_scripts': [
            'medrag-cli=src.medrag:main',  # Example if you have a CLI
        ],
    },
)
