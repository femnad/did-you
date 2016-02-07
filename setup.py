#!/usr/bin/env python
import setuptools

setuptools.setup(
    name='did_you',
    packages=setuptools.find_packages(),
    include_package_data=True,
    entry_points={'console_scripts':
                  ['did_you_server = did_you.command:run_server']},
    )
