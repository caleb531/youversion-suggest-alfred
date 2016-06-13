# Project tasks (for use with invoke task runner)

import subprocess
from invoke import task


@task
def test(cover=False):
    if cover:
        # Run tests via coverage and generate reports if --cover flag is given
        code = subprocess.call(['coverage', 'run', '-m', 'nose', '--rednose'])
        # Only show coverage report if all tests have passed
        if code == 0:
            # Add blank line between test report and coverage report
            print('')
            subprocess.call(['coverage', 'report'])
            subprocess.call(['coverage', 'html'])
    else:
        # Otherwise, run tests via nose (which is faster)
        code = subprocess.call(['nosetests', '--rednose'])


@task
def update(export=False, version=None):
    proc_args = ['workflow-packager', 'utilities/workflow_packager.json']
    if export:
        proc_args.append('--export')
    if version:
        proc_args.append('--version')
        proc_args.append(version)
    subprocess.call(proc_args)
