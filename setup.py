"""
Euchre python modules.

Nathaniel Lacelle <natelac@umich.edu>
"""

from setuptools import setup, find_packages

# TODO: What is name vs packages? What should these be?
setup(
    name='euchre',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'euchre-server = euchre.server:main',
            'euchre-console = euchre.players.online.console:main'
        ]
    },
)
