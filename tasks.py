#!/usr/bin/env python2

import os
import subprocess
from invoke import task


@task
def test():
    env = os.environ.copy()
    # Colorize nose output using rednose if available
    env.update({
        'NOSE_REDNOSE': '1'
    })
    subprocess.call(['coverage', 'run', '-m', 'nose'], env=env)


@task
def cover():
    subprocess.call(['coverage', 'report'])
    subprocess.call(['coverage', 'html'])
