#!/usr/bin/env python
import os
import sys

import django
from django.conf import settings
from django.test.utils import get_runner
#import ptvsd

#import ptvsd

os.sys.path.insert(0, os.getcwd())
#tvsd.enable_attach(secret='ischooldev', address=('0.0.0.0', 5678))

os.environ['DJANGO_SETTINGS_MODULE'] = 'ischool_profiles_api.settings'
django.setup()
TestRunner = get_runner(settings)
test_runner = TestRunner()
failures = test_runner.run_tests(["ischool_profiles_core", "ischool_profiles_api"])

sys.exit(bool(failures))