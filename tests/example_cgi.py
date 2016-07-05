#!/usr/bin/env python
# encoding: utf8

import sys
import os
import json

print("Content-Type: application/json")
print("")

data = {
    'greeting': "Hello from {0}".format(sys.argv[0]),
    'args': sys.argv[1:],
    'env': dict(os.environ),
    'body': sys.stdin.read()
}
print(json.dumps(data, indent=4))
