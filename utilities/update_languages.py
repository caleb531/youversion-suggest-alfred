# utilities.update_languages

# This language utility updates all existing Bible data files

from __future__ import unicode_literals

import glob
import re

from update_language import update_language


def main():

    for file_path in glob.iglob('yvs/data/bible/language-*.json'):
        language_id = re.search('language-(.*?).json', file_path).group(1)
        update_language(language_id)
        print('')


if __name__ == '__main__':
    main()
