#!/usr/bin/env python3

from invoke import task
import subprocess


@task
def test():
    nosetests = subprocess.Popen(['nosetests', '--rednose'])
    nosetests.wait()


@task
def cover():
    nosetests = subprocess.Popen(['nosetests', '--with-coverage',
                                  '--cover-erase', '--cover-html'])
    nosetests.wait()
