#!/usr/bin/env python3

import argparse
import configparser


def read_version():
    '''Read version from the ini file.'''
    try:
        config = configparser.ConfigParser()
        config.read('version.ini')
        return config['default']['version']
    except:
        raise


def write_version(version):
    '''Write version to the ini file.'''
    try:
        config = configparser.ConfigParser()
        config['default'] = {'version': version}
        with open('version.ini', 'w') as f:
            config.write(f)
    except:
        raise


def parse_version():
    '''Parse version as a command line argument.'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', type=str, nargs='?',
                        default=read_version, const=read_version)
    args = parser.parse_args()
    return args.version


if __name__ == '__main__':
    version = parse_version()
    write_version(version)
