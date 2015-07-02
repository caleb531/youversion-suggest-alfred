#!/usr/bin/env python

import subprocess
from invoke import task


@task
def test():
    subprocess.call(['coverage', 'run', '-m', 'nose', '--rednose'])


@task
def cover():
    subprocess.call(['coverage', 'report'])
    subprocess.call(['coverage', 'html'])
