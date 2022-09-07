from setuptools import setup, find_packages

setup(
    name='vending_machine',
    version='0.1.0',
	packages=find_packages(),
	include_package_data=True,
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'vending_machine = src.app.cli:cli',
        ],
    },
)