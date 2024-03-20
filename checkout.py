import json
import os
from os import path as osp
import re
import subprocess
import sys

projects = ['chart', 'closure', 'lang', 'math', 'time']

def print_err_and_exit(name):
    print("Usage: python3 {} [-p <project> OR -v <version>]".format(name))
    print("where\n\t<project> in [chart, closure, lang, math, time]\nand\n\t<version> = <project>_<nr>")
    exit(-1)

def powerset(s):
    x = len(s)
    masks = [1 << i for i in range(x)]
    for i in range(1 << x):
        yield [ss for mask, ss in zip(masks, s) if i & mask]

def dump_versions(proj):
    fault_dir = json.load(open(osp.join(os.environ['D4J_HOME'],
      "framework/bin/config.json")))['FAULT_DIR']
    name = proj.capitalize()
    if (not osp.isfile(osp.join(fault_dir, name+".json"))):
        print("ERROR: project", name, "not found")
        quit()
    sys.path.append(osp.join(os.environ['D4J_HOME'], "framework", "bin"))
    from backtrack import backtrack
    test_case_versions = open(osp.join(fault_dir, name+".json"))
    js = json.loads(test_case_versions.read())

    location_versions = open(osp.join(fault_dir, name+"_backtrack.json"))
    loc_js = json.loads(location_versions.read())
    versions = []
    for key in js.keys():
        faults = [int(key)]
        for val in js[key].keys():
            if (val != key):
                faults.append(int(val))
        faults.sort()
        s = name
        for fault in faults:
            if not backtrack(name, str(fault), str(key)).startswith("Bug not found"):
                s += "-"+str(fault)
        versions.append(s)
    return versions

def checkout(ver, dir):
    os.system('defects4j_multi checkout -v {} -w /tmp/{}'.format(ver, dir))

if __name__ == '__main__':
    # Reference: https://stackoverflow.com/questions/31807882/get-java-version-number-from-python#31808419
    output = str(subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT))
    pattern = '\"(\d+\.\d+).*\"'
    version = re.search(pattern, output).groups()[0]

    if version != '1.8':
        print("Java version must be 1.8")
        exit(-1)

    if len(sys.argv) < 3:
        print_err_and_exit(sys.argv[0])

    if sys.argv[1] == '-p':
        proj = sys.argv[2]
        if proj not in projects:
            print_err_and_exit(sys.argv[0])
        
        versions = dump_versions(proj)
        for ver in versions:
            nr = ver.split('-')[-1]
            dir = proj + '_' + nr
            checkout(ver, dir)
    elif sys.argv[1] == '-v':
        dir = sys.argv[2]
        proj, nr = dir.split(sep='_')
        if proj not in projects:
            print_err_and_exit(sys.argv[0])

        versions = dump_versions(proj)
        for ver in versions:
            if ver.endswith('-' + nr):
                checkout(ver, dir)
                break
    else:
        print_err_and_exit(sys.argv[0])