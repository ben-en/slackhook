from setuptools import setup

import slackhook as mod

setup(
    name='slackhook',
    version='0.1',
    author='Ben Ennis',
    author_email='ben@outernet.is',
    description='python script to interact with slack webhooks',
    packages=[mod.__name__],
    entry_points={
        'console_scripts': [
            'slackhook = slackhook.slackhook:main',
        ],
    },
)
