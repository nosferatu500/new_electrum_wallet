#!/usr/bin/env python3

# python setup.py sdist --format=zip,gztar

from setuptools import setup
import os
import sys
import platform
import imp
import argparse

version = imp.load_source('version', 'lib/version.py')


def readhere(path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, path), 'r') as fd:
        return fd.read()


def readreqs(path):
    return [req for req in
            [line.strip() for line in readhere(path).split('\n')]
            if req and not req.startswith(('#', '-r'))]


install_requires = readreqs('requirements.txt')
tests_requires = install_requires + readreqs('requirements_travis.txt')

if sys.version_info[:3] < (3, 4, 0):
    sys.exit("Error: Electrum requires Python version >= 3.4.0...")

data_files = []

if platform.system() in ['Linux', 'FreeBSD', 'DragonFly']:
    parser = argparse.ArgumentParser()
    parser.add_argument('--root=', dest='root_path', metavar='dir', default='/')
    opts, _ = parser.parse_known_args(sys.argv[1:])
    usr_share = os.path.join(sys.prefix, "share")
    if not os.access(opts.root_path + usr_share, os.W_OK) and \
       not os.access(opts.root_path, os.W_OK):
        if 'XDG_DATA_HOME' in os.environ.keys():
            usr_share = os.environ['XDG_DATA_HOME']
        else:
            usr_share = os.path.expanduser('~/.local/share')
    data_files += [
        (os.path.join(usr_share, 'applications/'), ['electrum.desktop']),
        (os.path.join(usr_share, 'pixmaps/'), ['icons/electrum.png'])
    ]

setup(
    name="Electrum-CRYP",
    version=version.ELECTRUM_VERSION,
    install_requires=install_requires,
    tests_require=tests_requires,
    packages=[
        'electrum',
        'electrum_gui',
        'electrum_gui.qt',
        'electrum_plugins',
        'electrum_plugins.audio_modem',
        'electrum_plugins.cosigner_pool',
        'electrum_plugins.email_requests',
        'electrum_plugins.greenaddress_instant',
        'electrum_plugins.hw_wallet',
        'electrum_plugins.keepkey',
        'electrum_plugins.labels',
        'electrum_plugins.ledger',
        'electrum_plugins.trezor',
        'electrum_plugins.digitalbitbox',
        'electrum_plugins.trustedcoin',
        'electrum_plugins.virtualkeyboard',
    ],
    package_dir={
        'electrum': 'lib',
        'electrum_gui': 'gui',
        'electrum_plugins': 'plugins',
    },
    package_data={
        'electrum': [
            'servers.json',
            'servers_testnet.json',
            'currencies.json',
            'checkpoints.json',
            'checkpoints_testnet.json',
            'www/index.html',
            'wordlist/*.txt',
            'locale/*/LC_MESSAGES/electrum.mo',
        ]
    },
    scripts=['electrum-cryp'],
    data_files=data_files,
    description="Lightweight CrypticCoin Wallet",
    license="MIT Licence",
    url="https://crypticcoin.io",
    long_description="""Lightweight CrypticCoin Wallet"""
)
