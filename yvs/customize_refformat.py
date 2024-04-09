#!/usr/bin/env python3
# coding=utf-8

import json
import os
import re

import yvs.core as core
import yvs.filter_prefs as filter_prefs


def main(variables):
    ref = core.get_ref("111/jhn.11.35", core.get_default_user_prefs())
    ref_format = json.loads(variables["value_id"])
    print(
        json.dumps(
            {
                "response": re.sub(
                    r"\s*¬\s*",
                    "\n",
                    filter_prefs.get_ref_format_value(ref_format, ref)["name"],
                ),
                "footer": " · ".join(
                    (
                        "Press enter to confirm {}".format(variables["pref_name"]),
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
    main(
        {
            "pref_id": os.environ["pref_id"],
            "pref_name": os.environ["pref_name"],
            "value_id": os.environ["value_id"],
            "value_name": os.environ["value_name"],
        }
    )
