from setuptools import setup, find_packages

setup(
    name='Accounts_Companion',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'appStart = Accounts_Companion.core:main',
        ],
    },
)