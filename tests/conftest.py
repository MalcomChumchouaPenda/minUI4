
import os
import sys

test_dir = os.path.dirname(__file__)
root_dir = os.path.dirname(test_dir)
if root_dir not in sys.path:
    sys.path.append(root_dir)
    