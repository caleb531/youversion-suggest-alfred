# utilities.update_workflow

# This workflow utility updates the installed workflow's scripts/resources with
# their latest versions. Passing the --export flag will also export the
# installed workflow to the local project directory.

import argparse
import biplist
import distutils.dir_util as distutils
import filecmp
import hashlib
import glob
import json
import plistlib
import os
import os.path
import re
import shutil
from zipfile import ZipFile, ZIP_DEFLATED


# Path to the current user's home directory
# The miminum depth a README section must be at in order to be numbered
MIN_README_SECTION_DEPTH = 2


# Retrieves correct path to directory containing Alfred's user preferences
def get_user_prefs_dir(alfred_version):

    library_dir = os.path.join(os.path.expanduser('~'), 'Library')
    core_prefs = biplist.readPlist(os.path.join(
        library_dir, 'Preferences',
        'com.runningwithcrayons.Alfred-Preferences-{}.plist'.format(
            alfred_version)))

    # If user is syncing their preferences using a syncing service
    if 'syncfolder' in core_prefs:
        return os.path.expanduser(core_prefs['syncfolder'])
    else:
        return os.path.join(
            library_dir, 'Application Support',
            'Alfred {}'.format(alfred_version))


# Retrieves path to and info.plist object for installed workflow
def get_installed_workflow(alfred_version, workflow_bundle_id):

    # Retrieve list of the directories for all installed workflows
    workflow_dirs = glob.iglob(os.path.join(
        get_user_prefs_dir(alfred_version), 'Alfred.alfredpreferences',
        'workflows', '*'))

    # Find workflow whose bundle ID matches this workflow's
    for workflow_dir in workflow_dirs:
        info_path = os.path.join(workflow_dir, 'info.plist')
        info = plistlib.readPlist(info_path)
        if info['bundleid'] == workflow_bundle_id:
            return workflow_dir, info

    # Assume workflow is not installed at this point
    raise OSError('YouVersion Suggest is not installed locally')


# Returns True if the item counts for the given directories match; otherwise,
# returns False
def check_dir_item_count_match(dir_path, dest_dir_path, dirs_cmp):

    return (not dirs_cmp.left_only and not dirs_cmp.right_only and
            not dirs_cmp.funny_files)


# Returns True if the contents of all files in the given directories match;
# otherwise, returns False
def check_dir_file_content_match(dir_path, dest_dir_path, dirs_cmp):

    match, mismatch, errors = filecmp.cmpfiles(
        dir_path, dest_dir_path, dirs_cmp.common_files, shallow=False)
    return not mismatch and not errors


# Returns True if the contents of all subdirectories (found recursively) match;
# otherwise, returns False
def check_subdir_content_match(dir_path, dest_dir_path, dirs_cmp):

    for common_dir in dirs_cmp.common_dirs:
        new_dir_path = os.path.join(dir_path, common_dir)
        new_dest_dir_path = os.path.join(dest_dir_path, common_dir)
        if not dirs_are_equal(new_dir_path, new_dest_dir_path):
            return False
    return True


# Recursively checks if two directories are exactly equal in terms of content
def dirs_are_equal(dir_path, dest_dir_path):

    dirs_cmp = filecmp.dircmp(dir_path, dest_dir_path)

    if not check_dir_item_count_match(dir_path, dest_dir_path, dirs_cmp):
        return False
    if not check_dir_file_content_match(dir_path, dest_dir_path, dirs_cmp):
        return False
    if not check_subdir_content_match(dir_path, dest_dir_path, dirs_cmp):
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

    if not resources_are_equal(resource_path, dest_resource_path):
        try:
            distutils.copy_tree(resource_path, dest_resource_path)
        except distutils.DistutilsFileError:
            shutil.copy(resource_path, dest_resource_path)
        print('Updated {}'.format(resource_path))


# Create parent directories in the installed workflow for the given resource
def create_resource_dirs(resource_patt, workflow_path):
    resource_dir = os.path.dirname(resource_patt)
    if resource_dir:
        workflow_resource_dir = os.path.join(workflow_path, resource_dir)
        try:
            os.makedirs(workflow_resource_dir)
        except OSError:
            pass


# Copies all package resources to installed workflow
def copy_pkg_resources(workflow_path, workflow_resources):

    for resource_patt in workflow_resources:
        for resource_path in glob.iglob(resource_patt):
            create_resource_dirs(resource_path, workflow_path)
            dest_resource_path = os.path.join(workflow_path, resource_path)
            copy_resource(resource_path, dest_resource_path)


# Operates on the section number stack according to the given section depth
def update_section_stack(stack, section_depth):
    current_depth = len(stack)
    if section_depth > current_depth:
        stack.append(1)
    else:
        for i in xrange(current_depth - section_depth):
            stack.pop()
        stack[-1] += 1


# Numbers MD sections by replacing # headings with numbered headings
def number_md_sections(content):

    stack = []
    lines = content.splitlines()
    for l, line in enumerate(lines):
        section_depth = (len(re.search('#*', line).group(0)) -
                         MIN_README_SECTION_DEPTH + 1)
        if section_depth > 0:
            update_section_stack(stack, section_depth)
            lines[l] = re.sub(
                '^#+', '{}.'.format('.'.join(map(str, stack))), line)
        else:
            lines[l] = re.sub('^#+ ', '', line)

    return '\n'.join(lines)


# Converts the given Markdown content to plain text
def convert_md_to_text(md_content):

    text_content = md_content
    # Convert backticks for code blocks to ''
    text_content = re.sub(r'`', '\'', text_content)
    # Remove formatting characters (except for - to denote lists)
    text_content = re.sub(r'(?<!\\)[*_~]', '', text_content)
    # Remove images
    text_content = re.sub(r'!\[(.*?)\]\((.*?)\)', '', text_content)
    # Reformat links
    text_content = re.sub(r'\[\]\((.*?)\)', '', text_content)
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
    text_content = re.sub(r' ?\n ?', '\n', text_content)
    # Number Markdown sections (marked by # headings)
    text_content = number_md_sections(text_content)

    return text_content


# Updates the workflow README with the current project README
def update_workflow_readme(info):

    with open('README.md', 'r') as readme_file:
        readme_md = readme_file.read()
    orig_readme_hash = hashlib.sha1(info['readme']).hexdigest()
    info['readme'] = convert_md_to_text(readme_md)
    if orig_readme_hash != hashlib.sha1(info['readme']).hexdigest():
        print('Updated workflow README')


# Sets the workflow version to a new version number if one is given
def update_workflow_version(info, new_version_num):
    if new_version_num:
        info['version'] = new_version_num
        print('Set version to v{}'.format(new_version_num))


# Writes installed workflow subdirectory files to the given zip file
def zip_workflow_dir_files(workflow_path, zip_file,
                           root, relative_root, files):
    for file_name in files:
        file_path = os.path.join(root, file_name)
        # Get path to current file relative to workflow directory
        relative_file_path = os.path.join(relative_root, file_name)
        zip_file.write(file_path, relative_file_path)


# Writes installed workflow subdirectories to the given zip file
def zip_workflow_dirs(workflow_path, zip_file):
    # Traverse installed workflow directory
    for root, dirs, files in os.walk(workflow_path):
        # Get current subdirectory path relative to workflow directory
        relative_root = os.path.relpath(root, workflow_path)
        # Add subdirectory to archive and add files within
        zip_file.write(root, relative_root)
        zip_workflow_dir_files(
            workflow_path, zip_file, root, relative_root, files)


# Exports installed workflow to project directory
def export_workflow(workflow_path, archive_path):

    # Create new Alfred workflow archive in project directory
    # Overwrite any existing archive
    with ZipFile(archive_path, 'w', compression=ZIP_DEFLATED) as zip_file:
        zip_workflow_dirs(workflow_path, zip_file)


def parse_cli_args():

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_path',
        help='the path to the utility configuration for this project')
    parser.add_argument(
        '--export', action='store_true',
        help='exports the installed workflow to the local project directory')
    parser.add_argument(
        '--version',
        help='the new version number to use for the workflow')
    return parser.parse_args()


# Locate and parse the configuration for the utility
def get_utility_config(config_path):
    with open(config_path, 'r') as config_file:
        return json.load(config_file)


def main():

    cli_args = parse_cli_args()
    config = get_utility_config(cli_args.config_path)

    project_path = os.getcwd()
    workflow_path, info = get_installed_workflow(
        config['alfred_version'], config['workflow_bundle_id'])

    copy_pkg_resources(workflow_path, config['workflow_resources'])
    update_workflow_readme(info)
    update_workflow_version(info, cli_args.version)
    plistlib.writePlist(info, os.path.join(workflow_path, 'info.plist'))

    if cli_args.export:
        export_workflow(workflow_path, os.path.join(
            project_path, config['exported_workflow']))
        print('Exported installed workflow successfully (v{})'.format(
            info['version']))

if __name__ == '__main__':
    main()
