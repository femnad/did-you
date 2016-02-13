#!/usr/bin/env python
import setuptools

setuptools.setup(
    name='did_you',
    packages=setuptools.find_packages(),
    include_package_data=True,
    data_files = [
        ('/config/did_you.conf.sample'), ('/usr/local/etc/did_you.conf')],
    entry_points={'console_scripts':
                  ['did_you_server = did_you.command:run_server']},
    )
