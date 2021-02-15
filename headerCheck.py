#!/usr/bin/env python3
# Copyright (c) 2021 Elliot Powell
# SPDX-License-Identifier: MIT
import sys, os, re, datetime, getopt

# REGEX FILE EXTENSTIONS FOR /*...*/ FORMATED COPYRIGHT
headerOneFiles = ["\.c", "\.h", "\.keymap", "\.dts", "\.overlay", "\.dtsi"]
# REGEX STRINGS FOR ANY FILES WHICH SHOULD BE IGNORED FROM CHECKING
regexIgnored = ["\.yaml", "\.md", "\.json", "\.yml", "\.js", "ignore", "\.prettier", "\.toml"] 


# COLOURS FOR OUTPUT FORMATIING
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
incorrectFiles = []

# use --main to check against origin main for all new files else just checks cached e.g. during a commit
toCheck = "origin/main HEAD" if "--main" in sys.argv else "--cached"

newlyAddedFiles=os.popen(f"git diff --name-only --diff-filter=A {toCheck}").read().split("\n")[:-1]
modifiedFiles=os.popen(f"git diff --name-only --diff-filter=M {toCheck}").read().split("\n")[:-1]
#print("Newly added files: ", newlyAddedFiles)
#print("Modified Files: ", modifiedFiles)

# function to check wether a file should be ignored when checking
def isIgnored(name):
    for i in regexIgnored:
        if re.search(rf'{i}', name): 
            return True
    return False


# function to return the appropriate header regex to check for
def header(fileName, yearToUse):
    for i in headerOneFiles:
        if re.search(rf'{i}', fileName): 
            return f"\/\*\n \* Copyright \(c\) {yearToUse} \w.*\n \*\n \* SPDX-License-Identifier: MIT\n \*\/"
    return f"# Copyright \(c\) {yearToUse}.*\n# SPDX-License-Identifier: MIT"


def check(status, file):
    y = year
    if status=="m": y="202[0-9]"
    license = header(file, y)
    with open(file) as checkFile:
        # try to read the first 5 lines however if files is shorter than this we check the whole file
        try:
            head = ''.join([next(checkFile) for x in range(5)])
        except:
            head = ''.join([next(checkFile) for x in checkFile])
    if (not re.search(license, head)): incorrectFiles.append(file)
    


def main():
    for newlyAddedFile in newlyAddedFiles:
        if isIgnored(newlyAddedFile): continue
        check("n", newlyAddedFile)

    for modifiedFile in modifiedFiles:
        if isIgnored(modifiedFile): continue
        check("m", modifiedFile)

        
    if (not incorrectFiles):
        print(f"{colours.OKGREEN}All headers correct on newly added and modified files{colours.ENDC}")
        sys.exit()
    else:
        print(f"{colours.FAIL}Incorrect File Headers on the following new or modified Files:{colours.ENDC}")
        for file in incorrectFiles:
            print(f"  -  {file}")
        sys.exit(2)

main()