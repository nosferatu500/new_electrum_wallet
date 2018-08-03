"""
py2app build script for Electrum Bitcoin Private

Usage (Mac OS X):
     python setup.py py2app
"""

from setuptools import setup
from plistlib import Plist
import requests
import os
import shutil

from lib.version import ELECTRUM_VERSION as version

CERT_PATH = requests.certs.where()

name = "Electrum CRYP"
mainscript = 'electrum-cryp'

plist = Plist.fromFile('Info.plist')
plist.update(dict(CFBundleIconFile='icons/electrum.icns'))


os.environ["REQUESTS_CA_BUNDLE"] = "cacert.pem"
shutil.copy(mainscript, mainscript + '.py')
mainscript += '.py'
extra_options = dict(
    setup_requires=['py2app'],
    app=[mainscript],
    packages=[
        'electrum-cryp',
        'electrum-cryp_gui',
        'electrum-cryp_gui.qt',
        'electrum-cryp_plugins',
        'electrum-cryp_plugins.audio_modem',
        'electrum-cryp_plugins.cosigner_pool',
        'electrum-cryp_plugins.email_requests',
        'electrum-cryp_plugins.greenaddress_instant',
        'electrum-cryp_plugins.hw_wallet',
        'electrum-cryp_plugins.keepkey',
        'electrum-cryp_plugins.labels',
        'electrum-cryp_plugins.ledger',
        'electrum-cryp_plugins.trezor',
        'electrum-cryp_plugins.digitalbitbox',
        'electrum-cryp_plugins.trustedcoin',
        'electrum-cryp_plugins.virtualkeyboard',

    ],
    package_dir={
        'electrum-cryp': 'lib',
        'electrum-cryp_gui': 'gui',
        'electrum-cryp_plugins': 'plugins'
    },
    data_files=[CERT_PATH],
    options=dict(py2app=dict(argv_emulation=False,
                             includes=['sip'],
                             packages=['lib', 'gui', 'plugins'],
                             iconfile='icons/electrum.icns',
                             plist=plist,
                             resources=["icons"])),
)

setup(
    name=name,
    version=version,
    **extra_options
)

# Remove the copied py file
os.remove(mainscript)
