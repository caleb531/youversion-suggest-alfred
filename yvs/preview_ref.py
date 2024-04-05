#!/usr/bin/env python3
# coding=utf-8

import json
import re
import sys

import yvs.copy_ref as copy_ref
import yvs.core as core


# Display the correct message for whichever default action is set based on the
# user's copybydefault preference
def get_default_action_message(user_prefs):
    if user_prefs["copybydefault"]:
        return "↩ Copy content to clipboard"
    else:
        return "↩ View on YouVersion"


def main(ref_uid):

    # For the preview mode, we want to ignore the user's preferred reference
    # format so that we can always display the reference address consistently at
    # the top of the text view
    user_prefs = {
        **core.get_user_prefs(),
        "versenumbers": False,
        "linebreaks": True,
        "refformat": "## {name} ({version})\n\n{content}",
    }
    ref = core.get_ref(ref_uid, user_prefs)
    copied_ref = copy_ref.get_copied_ref_from_object(ref, user_prefs)
    full_ref_name = core.get_full_ref_name(ref)
    print(
        json.dumps(
            {
                # Because we are rendering the reference content as Markdown, we
                # need to add a double-space before each newline (but not
                # between consecutive newlines)
                "response": re.sub(r"(\n+)", (2 * " ") + r"\1", copied_ref),
                "footer": " · ".join(
                    (
                        full_ref_name,
                        get_default_action_message(user_prefs),
                        "⎋ Return to results",
                    )
                ),
                "behaviour": {
                    "response": "replace",
                    "scroll": "auto",
                },
            }
        )
    )


if __name__ == "__main__":
    main(sys.argv[1])
