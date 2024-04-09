#!/bin/bash

# The Alfred 5.5 Text View can only run an executable script as input; it cannot
# execute arbitrary script code, which we ultimately need to do so we can run
# the yvs.customize_refformat as a module; therefore, this intermediate shell
# script is necessary to run yvs.customize_refformat in the proper module
# context
/usr/bin/python3 -m yvs.customize_refformat "$@"
