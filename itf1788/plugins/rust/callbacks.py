#
# #
#                              ITF1788
#
#   Interval Test Framework for IEEE 1788 Standard for Interval Arithmetic
#
#
#   Copyright 2014
#
#   Marco Nehmeier (nehmeier@informatik.uni-wuerzburg.de)
#   Maximilian Kiesner (maximilian.kiesner@stud-mail.uni-wuerzburg.de)
#
#   Department of Computer Science
#   University of Wuerzburg, Germany
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import re

#
# Input: the string of an integral number as defined in the ITL file
# Output: the required representation for the target test file as a string
#


def cb_int(val):
    return repr(float(val))

#
# Input: the string of a floating point number as defined in the ITL file
# Output: the required representation for the target test file as a string
#


def cb_fpNum(val):
    if 'p' in val.lower():
        return repr(float.fromhex(val))
    else:
        return repr(float(val))

#
# Input: a string as defined in the ITL file
# Output: the required representation of the string in the target test file
#


def cb_string(val):
    return val

#
# Input: the string of a qualified identifier as defined in the ITL file
# Output: the required representation for the target test file as a string
#


def cb_qualident(val):
    return val.replace('.', '_').lower()

#
# Input: the name of a input variable as a string. In its unmodified
#        form, it looks like "inp_x_y" where "x" indicates the test
#        number and "y" the ordinal of the variable within that test.
#        Thus "inp_4_3" is the third input variable
#        in the fourth test (which contains array literals).
# Output: the required representation of the variable name
#


def cb_inp_var_name(val):
    return val

#
# Input: the name of a output variable as a string. In its unmodified
#        form, it looks like "outp_x_y" where "x" indicates the test
#        number and "y" the ordinal of the variable within that test.
#        Thus "outp_4_3" is the third output variable
#        in the fourth test (which contains array literals).
# Output: the required representation of the variable name
#


def cb_outp_var_name(val):
    return val
