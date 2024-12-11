#!/usr/bin/python3
import sys
lazy_paginator = __import__('2-lazy_paginate').lazy_paginate

try:
    for page in lazy_paginator(100):  # Fetch data in pages of 100 rows
        for user in page:
            print(user)
except BrokenPipeError:
    sys.stderr.close()
