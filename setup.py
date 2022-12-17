"""
Euchre python modules.

Nathaniel F. Lacelle <natelac@umich.edu>
"""

from setuptools import setup, find_packages

setup(
    name='euchre',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'numpy',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'euchre-server = euchre.server.mainserver:main',
            'euchre-webconsole = euchre.clients.webconsole.webconsole:main',
            'euchre-play = euchre.play:play'
        ]
    },
)
