import os
import re
import subprocess
import sys

# Reference: https://stackoverflow.com/questions/31807882/get-java-version-number-from-python#31808419
output = str(subprocess.check_output(['java', '-version'], stderr=subprocess.STDOUT))
pattern = '\"(\d+\.\d+).*\"'
version = re.search(pattern, output).groups()[0]

if version != '1.8':
    print("Java version must be 1.8")
    exit(-1)

path = os.getcwd()
d4j_path = path + '/defects4j'

if not os.path.isdir(d4j_path):
    os.system('git clone https://github.com/rjust/defects4j.git')
    os.chdir('defects4j')
    os.system('cpanm --installdeps .')
    os.system('./init.sh')
else:
    os.chdir('defects4j')

if os.path.isfile(os.path.join(os.environ['HOME'], ".bashrc")):
    rcfile = open(os.path.join(os.environ['HOME'], ".bashrc"), "a")
else:
    rcfile = open(os.path.join(os.environ['HOME'], ".profile"), "a")
rcfile.write('export D4J_HOME="{}"\n'.format(d4j_path))
rcfile.write('export PATH="$PATH:$D4J_HOME/framework/bin"\n')
rcfile.close()
os.system('export PATH=$PATH:{}/framework/bin'.format(d4j_path))

if '--check' in sys.argv:
    # Check Defects4J installation
    lang = os.popen('defects4j info -p Lang').read()
    print(lang)

os.system('git apply {}/defects4j_multi_with_jars.patch'.format(path))
os.system('export D4J_HOME={}'.format(d4j_path))
os.chdir('..')

if '--check' in sys.argv:
    # Check multifault Defects4J installation
    d4jm = os.popen('defects4j_multi -h').read()
    with open('d4jm.txt') as file:
        contents = file.read()
        if d4jm != contents:
            print("Incorrect installation of multifault Defects4J")
            exit(-1)
        else:
            print("Multifault Defects4J correctly installed")

os.chdir('fault_data')
os.system('tar -xjf multi.tar.bz2')
os.system('defects4j_multi configure -f {}/fault_data'.format(path))
