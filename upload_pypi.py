""" Uploads wheels to pypi from travisci.

The commit requires an UPLOAD line.
"""
import glob
import os
import subprocess
import sys

# Set these inside travis. Note, it is on a per repo basis.
# https://docs.travis-ci.com/user/environment-variables/#Encrypting-Variables-Using-a-Public-Key
# travis encrypt PYPI_USERNAME=super_secret --add env.matrix
# travis encrypt PYPI_PASSWD=super_secret --add env.matrix
username = os.environ['PYPI_USERNAME'],
password = os.environ['PYPI_PASSWD'],


commit = subprocess.check_output(['git', 'log', '-1'])

if b'+UPLOAD' not in commit:
    print('Not uploading')
    sys.exit(0)

# There should be exactly one .whl
filename = glob.glob('*.whl')[0]

pypirc_template = """\
[distutils]
index-servers =
    pypi
[pypi]
repository: https://upload.pypi.io/legacy/
username: {username}
password: {password}
""".format(username=username, password=password)

with open('pypirc', 'w') as f:
    f.write(pypirc_template)

print('Calling twine to upload...')
try:
    subprocess.check_call(['twine', 'upload', '--config-file', 'pypirc', filename])
finally:
    os.unlink('pypirc')
