#!/usr/bin/env python
from __future__ import print_function

import optparse
import os
import os.path
import re
import shutil
import sys

parser = optparse.OptionParser()
parser.add_option('-e', '--email', help='user_email')

(options, args) = parser.parse_args()

export_dir = '/ftp'

user_name = options.email.split('@')
dir_full_path = os.path.join(export_dir, user_name[0])

if len(args) < 3:
    parser.error('Require at least two arguments')
if len(args) % 3 != 0:
    parser.error('Require an even number of arguments')

real_export_dir = os.path.realpath(dir_full_path)

if not os.path.exists(export_dir):
    raise Exception("'%s' directory does not exist or it is not accessible by the Galaxy user" % export_dir)

# Create user dir
try: 
    os.makedirs(dir_full_path)
except OSError:
    if not os.path.isdir(dir_full_path):
        raise

dataset_paths = args[::3]
dataset_names = args[1::3]
dataset_exts = args[2::3]

exit_code = 0

for dp, dn, de in zip(dataset_paths, dataset_names, dataset_exts):
 
    dn_de = "%s.%s" % (dn, de)
    dn_de_safe = re.sub(r'(?u)[^-\w.]', '', dn_de.strip().replace(' ', '_'))
    dest = os.path.join(real_export_dir, dn_de_safe)
    try:
        shutil.copy2(dp, dest)
        print("Dataset '%s' copied to '%s'" % (dn, dest))
    except Exception as e:
        msg = "Error copying dataset '%s' to '%s', %s" % (dn, dest, e)
        print(msg, file=sys.stderr)
        exit_code = 1

sys.exit(exit_code)
