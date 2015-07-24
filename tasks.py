# Project tasks (for use with invoke task runner)

import subprocess
from invoke import task


@task
def test(cover=False):
    # Run tests using nose called with coverage
    code = subprocess.call(['coverage', 'run', '-m', 'nose', '--rednose'])
    # Also generate coverage reports when --cover flag is given
    if cover and code == 0:
        # Add blank line between test report and coverage report
        print('')
        subprocess.call(['coverage', 'report'])
        subprocess.call(['coverage', 'html'])


@task
def update(export=False):
    proc_args = ['python', '-m', 'utilities.update_workflow']
    if export:
        proc_args.append('--export')
    subprocess.call(proc_args)
