#!/usr/bin/python
import pip

_all_ = [
    "psutil==5.8.0",
    "freedeck-serial-api==0.0.4"
]

windows = ["pywin32==300", "wmi==1.5.1"]
linux = ["psutil==5.8.0", ]
darwin = []


def install(packages):
    for package in packages:
        pip.main(['install', package])


if __name__ == '__main__':

    from sys import platform

    install(_all_)
    if platform == 'windows':
        install(windows)
    if platform.startswith('linux'):
        install(linux)
    if platform == 'darwin':  # MacOS
        install(darwin)
