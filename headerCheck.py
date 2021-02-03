#!/usr/bin/env python3
import sys, os, re, datetime, getopt

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
        print(f"Copyright (c) {year} YOUR NAME license header not found in the following newly added files:")
        for file in noCopyright:
            print(f"  -  {file}")
    if noSPDX:
        print(f"SPDX-License-Identifier: MIT license header not found in the following newly added files:")
        for file in noSPDX:
            print(f"  -  {file}")
    sys.exit(1)