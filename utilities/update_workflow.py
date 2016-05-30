# utilities.update_workflow

# This workflow utility updates the installed workflow's scripts/resources with
# their latest versions. Passing the --export flag will also export the
# installed workflow to the local project directory.

import argparse
import biplist
import distutils.dir_util as distutils
import filecmp
import glob
import plistlib
import os
import os.path
import re
import shutil
from zipfile import ZipFile, ZIP_DEFLATED


# Name of the exported workflow file
WORKFLOW_NAME = 'YouVersion Suggest (Alfred 3).alfredworkflow'
# Path to the current user's home directory
HOME_DIR = os.path.expanduser('~')
# Name of Alfred's core preferences file
CORE_PREFS_NAME = 'com.runningwithcrayons.Alfred-Preferences-3.plist'
# Path to Alfred's core preferences file
CORE_PREFS_PATH = os.path.join(
    HOME_DIR, 'Library', 'Preferences', CORE_PREFS_NAME)
# Name of Alfred's user preferences file
USER_PREFS_NAME = 'Alfred.alfredpreferences'
# Path to the default location of Alfred's user preferences file
DEFAULT_USER_PREFS_DIR = os.path.join(
    HOME_DIR, 'Library', 'Application Support', 'Alfred 3')
# List of all files/directories to be copied to the exported workflow
PKG_RESOURCES = (
    'icon.png',
    'yvs/__init__.py',
    'yvs/shared.py',
    'yvs/data/bible',
    'yvs/data/defaults.json',
    'yvs/data/languages.json',
    'yvs/data/search-engines.json'
)


# Retrieves correct path to directory containing Alfred's user preferences
def get_user_prefs_dir():

    core_prefs = biplist.readPlist(CORE_PREFS_PATH)

    # If user is syncing their preferences using a syncing service
    if 'syncfolder' in core_prefs:
        return os.path.expanduser(core_prefs['syncfolder'])
    else:
        return DEFAULT_USER_PREFS_DIR


# Retrieves path to installed workflow
def get_workflow_path():

    # Assume that whichever workflow contains a 'yvs' directory is YV Suggest
    yvs_packages = glob.glob(os.path.join(
        get_user_prefs_dir(), USER_PREFS_NAME, 'workflows', '*', 'yvs'))

    if not yvs_packages:
        raise OSError('YouVersion Suggest in not installed locally')

    # Return the first (and presumably only) match found
    return os.path.dirname(yvs_packages[0])


# Retrieves the file content of a module withini the project
def get_module_content(module_name):

    file_name = '{}.py'.format(module_name.replace('.', '/'))
    with open(file_name, 'r') as file_obj:
        return file_obj.read()


# Retrieve the name of a module by parsing it from the module's content
def get_module_name(module_content):

    # The module name has been made accessible as a code comment on the first
    # line of the respective module's content
    first_line = module_content.split('\n', 1)[0]
    return first_line[1:].strip()


# Updates content of all scripts in workflow info object
def update_workflow_objects(info):

    updated_objects = []

    for obj in info['objects']:

        if 'script' in obj['config']:

            module_name = get_module_name(obj['config']['script'])
            new_module_content = get_module_content(module_name)

            if new_module_content != obj['config']['script']:
                obj['config']['script'] = new_module_content
                updated_objects.append(module_name)

    return updated_objects


# Recursively checks if two directories are exactly equal in terms of content
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


# Checks if resource (file or directory) is equal to destination resource
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


# Copies package resource to corresponding destination path
def copy_resource(resource_path, dest_resource_path):

    try:
        distutils.copy_tree(resource_path, dest_resource_path)
    except distutils.DistutilsFileError:
        shutil.copy(resource_path, dest_resource_path)


# Copies all package resources to installed workflow
def copy_pkg_resources(workflow_path):

    updated_resources = []

    for resource_path in PKG_RESOURCES:

        dest_resource_path = os.path.join(workflow_path, resource_path)
        # Only copy resources if content has changed
        if not resources_are_equal(resource_path, dest_resource_path):
            copy_resource(resource_path, dest_resource_path)
            updated_resources.append(resource_path)

    return updated_resources


# Converts the given Markdown content to plain text
def convert_md_to_text(md_content):

    text_content = md_content
    # Convert backticks for code blocks to ''
    text_content = re.sub(r'`', '\'', text_content)
    # Remove formatting characters (except for - to denote lists)
    text_content = re.sub(r'(?<!\\)[*#]', '', text_content)
    # Remove images
    text_content = re.sub(r'!\[(.*?)\]\((.*?)\)', '', text_content)
    # Reformat links
    text_content = re.sub(r'\[(.*?)\]\((.*?)\)', '\\1 (\\2)', text_content)
    # Remove backslashes
    text_content = re.sub(r'\\', '', text_content)
    # Remove leading/trailing whitespace
    text_content = text_content.strip()
    # Remove hard-wrapping from paragraphs
    text_content = re.sub(r'(?<![\-\s])\n(?![\-\s\d])', ' ', text_content)
    # Collapse whitespace
    text_content = re.sub(r' +', ' ', text_content)
    text_content = re.sub(r'\n\n+', '\n\n', text_content)
    text_content = re.sub(r'( *)\n( *)', '\n', text_content)

    return text_content


# Updates the workflow README with the current project README
def update_workflow_readme(info):

    with open('README.md', 'r') as readme_file:
        readme_md = readme_file.read()
    readme_text = convert_md_to_text(readme_md)
    original_readme_text = info['readme']
    info['readme'] = readme_text
    return original_readme_text != readme_text


# Exports installed workflow to project directory
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


# Prints a list of all the workflow objects that have been updated
def print_updated_objects(updated_objects):
    for module_name in updated_objects:
        print('Updated {}'.format(module_name))


# Prints a list of all the workflow resources that have been updated
def print_updated_resources(updated_resources):
    for resource_path in updated_resources:
        print('Updated {}'.format(resource_path))


# Check if workflow has any changes and print status messages if so
def check_workflow_for_updates(workflow_path, info_path, info):

    updated_objects = update_workflow_objects(info)
    updated_resources = copy_pkg_resources(workflow_path)
    did_update_readme = update_workflow_readme(info)
    did_update_workflow = False
    did_update_workflow_plist = False

    if updated_objects:
        did_update_workflow = True
        did_update_workflow_plist = True
        print_updated_objects(updated_objects)

    if updated_resources:
        did_update_workflow = True
        print_updated_resources(updated_resources)

    if did_update_readme:
        did_update_workflow = True
        did_update_workflow_plist = True
        print('Updated workflow README')

    if did_update_workflow_plist:
        plistlib.writePlist(info, info_path)

    if did_update_workflow:
        print('Updated installed workflow successfully')
    else:
        print('Workflow has not changed')


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

    info_path = os.path.join(workflow_path, 'info.plist')
    info = plistlib.readPlist(info_path)

    check_workflow_for_updates(workflow_path, info_path, info)

    if cli_args.export:
        export_workflow(workflow_path, project_path)
        print('Exported installed workflow successfully')

if __name__ == '__main__':
    main()
