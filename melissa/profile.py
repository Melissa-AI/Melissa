# Melissa
from profile_loader import load_profile

global data
data = {}

if len(data) == 0:
    # global data
    data = load_profile()
