#!/usr/bin/env python3
# Copyright (c) 2021 Elliot Powell
# SPDX-License-Identifier: MIT

import sys, os, re, datetime, getopt
class colours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

year = datetime.datetime.now().year 
regexIgnored = ["\.yaml", "\.md", "\.json", "\.yml"]
noCopyright = []
noSPDX = []
toCheck = "--cached"
# use --main to check against origin main for all new files else just checks cached e.g. during a commit
if "--main" in sys.argv:
    toCheck = "origin/main HEAD"

newlyAddedFiles=os.popen(f"git diff --name-only --diff-filter=A {toCheck}").read().split("\n")[:-1]
#print(newlyAddedFiles)

# simple function to check wether a file should be ignored when checking
def isIgnored(name):
    for i in regexIgnored:
        if re.search(rf'{i}', newlyAddedFile): 
            return True
    return False
           


for newlyAddedFile in newlyAddedFiles:
    if isIgnored(newlyAddedFile): continue
    # check only first 5 lines of the file
    if os.popen(f'head -5 {newlyAddedFile} | grep -L "Copyright (c) {year}" '): noCopyright.append(newlyAddedFile)
    if os.popen(f'head -5 {newlyAddedFile} | grep -L "SPDX-License-Identifier: MIT" '): noSPDX.append(newlyAddedFile)
    
if (not noCopyright) & (not noSPDX):
    print("All headers correct on newly added files")
    sys.exit()
else:
    print("Incorrect File Headers Found on newly added files")
    if noCopyright:
        print(f"{colours.FAIL}Copyright (c) {year} YOUR NAME license header not found in the following newly added files:{colours.ENDC}")
        for file in noCopyright:
            print(f"  -  {file}")
    if noSPDX:
        print(f"{colours.FAIL}SPDX-License-Identifier: MIT license header not found in the following newly added files:{colours.ENDC}")
        for file in noSPDX:
            print(f"  -  {file}")
    sys.exit("Failed, See log for more details")