from setuptools import setup, find_packages
from os import path, getenv
from sys import exit
from setuptools.command.install import install

here = path.abspath(path.dirname(__file__))

VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_BUGFIX = 1
VERSION_STRING = "{}.{}.{}".format(VERSION_MAJOR, VERSION_MINOR, VERSION_BUGFIX)

# TAG_ENV_VARIABLE = 'CIRCLE_TAG'
# TAG_VERSION_PREFIX = "celestial_tools_"

# Arguments marked as "Required" below must be included for upload to PyPI.
# Fields marked as "Optional" may be commented out.

'''
class VerifyVersionCommand(install):
    """Custom command to verify that the git tag matches our version"""
    description = 'verify that the git tag matches our version'

    def run(self):
        tag = getenv(TAG_ENV_VARIABLE, "")
        # Make sure the tag starts with "celestial_tools_
        if not tag.startswith(TAG_VERSION_PREFIX):
            info = "Git tag: {0} is not formatted correctly".format(
                tag
            )
            exit(info)
        # Make sure the version after "celestial_tools_" matches our VERSION_STRING
        if tag[len(TAG_VERSION_PREFIX):] != VERSION_STRING:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION_STRING
            )
            exit(info)
'''

setup(
    name='ntcip_relay_server',
    version=VERSION_STRING,
    description='NTCIP Relay Server',  # Optional
    # url='',
    author='Adam Schafer, Dan Walkes',
    author_email='danwalkes@trellis-logic.com',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(exclude=["tests"]),
    python_requires='>=3.6',
    install_requires=['flask>=1.1.2', 'easysnmp>=0.2.5'],
    extras_require={
        'test': ['coverage'],
    },
    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={

    },
    entry_points={
        'console_scripts': [
            'ntcip-relay-server=ntcip_relay_server.app.ntcip_relay_server:cmdline'
        ],
    },
    cmdclass={
        # 'verify_tag': VerifyVersionCommand,
    }
)
