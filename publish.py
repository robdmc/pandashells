import subprocess

subprocess.call('pip install wheel'.split())
subprocess.call('pip install twine'.split())
subprocess.call('rm -rf ./build'.split())
subprocess.call('rm -rf ./dist/'.split())
subprocess.call('python setup.py clean --all'.split())
subprocess.call('python setup.py sdist bdist_wheel'.split())
subprocess.call('twine upload dist/*'.split())
