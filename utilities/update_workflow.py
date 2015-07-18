# utilities.update_workflow
# This workflow utility updates all workflow resources with the latest versions
# found in this repository. Passing the --export flag will also export the
# installed workflow to the local project directory.

import argparse
import biplist
import contextlib
import distutils.dir_util as distutils
import filecmp
import glob
import plistlib
import os
import os.path
import shutil
from zipfile import ZipFile, ZIP_DEFLATED


WORKFLOW_NAME = 'YouVersion Suggest.alfredworkflow'
HOME_DIR = os.path.expanduser('~')
CORE_PREFS_NAME = 'com.runningwithcrayons.Alfred-Preferences.plist'
USER_PREFS_NAME = 'Alfred.alfredpreferences'
DEFAULT_USER_PREFS_DIR = os.path.join(
    HOME_DIR, 'Library', 'Application Support', 'Alfred 2')
PKG_RESOURCES = ('icon.png', 'yvs/__init__.py', 'yvs/shared.py', 'yvs/data')


# Get path to directory containing Alfred's user preferences
def get_user_prefs_dir():

    core_prefs = biplist.readPlist(
        os.path.join(HOME_DIR, 'Library', 'Preferences', CORE_PREFS_NAME))

    # If user is syncing their preferences using a syncing service
    if 'syncfolder' in core_prefs:
        return os.path.expanduser(core_prefs['syncfolder'])
    else:
        return DEFAULT_USER_PREFS_DIR


# Get path to Alfred's user preferences file
def get_user_prefs_path():

    return os.path.join(get_user_prefs_dir(), USER_PREFS_NAME)


# Get path to installed workflow
def get_workflow_path():

    yvs_packages = glob.glob(
        os.path.join(get_user_prefs_path(), 'workflows', '*', 'yvs'))

    if len(yvs_packages) == 0:
        raise OSError('YouVersion Suggest in not installed locally')

    return os.path.dirname(yvs_packages[0])


# Get path to installed workflow's info.plist file
def get_workflow_info_path(workflow_path):

    return os.path.join(workflow_path, 'info.plist')


# Parse the info.plist file at the given path
def get_workflow_info(info_path):

    return plistlib.readPlist(info_path)


# Get the file content of a module withini the project
def get_module_content(module_name):

    file_name = '{}.py'.format(module_name.replace('.', '/'))
    with open(file_name, 'r') as file:
        return file.read()


# Get the name of a module by parsing it from the module content
def get_module_name(module_content):

    first_line = module_content.split('\n', 1)[0]
    module_name = first_line[1:].strip()
    return module_name


# Update content of all scripts in workflow info object
def update_workflow_objects(info):

    updated_objects = False

    for obj in info['objects']:

        if 'script' in obj['config']:

            module_name = get_module_name(obj['config']['script'])
            new_module_content = get_module_content(module_name)

            if new_module_content != obj['config']['script']:
                obj['config']['script'] = new_module_content
                print 'Updated {}'.format(module_name)
                updated_objects = True

    return updated_objects


# Recursively check if two directories are exactly equal in terms of content
def dirs_are_equal(dir_path, dest_dir_path):

    dirs_cmp = filecmp.dircmp(dir_path, dest_dir_path)
    if len(dirs_cmp.left_only) > 0 or len(dirs_cmp.right_only) > 0:
        return False

    match, mismatch, errors = filecmp.cmpfiles(
        dir_path, dest_dir_path, dirs_cmp.common_files, shallow=False)
    if len(mismatch) > 0 or len(errors) > 0:
        return False

    for common_dir in dirs_cmp.common_dirs:
        new_dir_path = os.path.join(dir_path, common_dir)
        new_dest_dir_path = os.path.join(dest_dir_path, common_dir)
        if not dirs_are_equal(new_dir_path, new_dest_dir_path):
            return False

    return True


# Check if resource (file or directory) is equal to destination resource
def resources_are_equal(resource_path, dest_resource_path):

    try:
        return dirs_are_equal(resource_path, dest_resource_path)
    except OSError:
        # Compare files if they are not directories
        try:
            return filecmp.cmp(resource_path, dest_resource_path)
        except OSError:
            # Resources are not equal if either does not exist
            return False


# Copy package resource (file or directory) to corresponding destination path
def copy_resource(resource_path, dest_resource_path):

    try:
        distutils.copy_tree(resource_path, dest_resource_path)
    except distutils.DistutilsFileError:
        shutil.copy(resource_path, dest_resource_path)


# Copy all package resources (files or directories) to installed workflow
def copy_pkg_resources(workflow_path):

    updated_resources = False

    for resource_path in PKG_RESOURCES:

        dest_resource_path = os.path.join(workflow_path, resource_path)
        # Only copy resources if content has changed
        if not resources_are_equal(resource_path, dest_resource_path):
            copy_resource(resource_path, dest_resource_path)
            print 'Updated {}'.format(resource_path)
            updated_resources = True

    return updated_resources


# Write info.plist object to file
def save_info(info, info_path):

    plistlib.writePlist(info, info_path)
    print 'Updated info.plist'


# Export installed workflow to project directory
def export_workflow(workflow_path, project_path):

    archive_path = os.path.join(project_path, WORKFLOW_NAME)
    # Create new Alfred workflow archive in project directory
    # Overwrite any existing archive
    with ZipFile(archive_path, 'w', compression=ZIP_DEFLATED) as zip_file:
        # Traverse installed workflow directory
        for root, dirs, files in os.walk(workflow_path):
            # Get current subdirectory path relative to workflow directory
            relative_root = os.path.relpath(root, workflow_path)
            # Add subdirectory to archive and add files within
            zip_file.write(root, relative_root)
            for file_name in files:
                file_path = os.path.join(root, file_name)
                # Get path to current file relative to workflow directory
                relative_file_path = os.path.join(relative_root, file_name)
                zip_file.write(file_path, relative_file_path)


def parse_cli_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--export', action='store_true',
        help='exports the installed workflow to the local project directory')

    return parser.parse_args()


def main():

    cli_args = parse_cli_args()
    project_path = os.getcwd()
    workflow_path = get_workflow_path()
    info_path = get_workflow_info_path(workflow_path)
    info = get_workflow_info(info_path)
    updated_objects = update_workflow_objects(info)
    updated_resources = copy_pkg_resources(workflow_path)
    if updated_objects or updated_resources:
        save_info(info, info_path)
        print 'Updated installed workflow successfully'
    else:
        print 'Workflow has not changed'
    if cli_args.export:
        export_workflow(workflow_path, project_path)
        print 'Exported workflow successfully'

if __name__ == '__main__':
    main()
