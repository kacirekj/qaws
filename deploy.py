import os

os.system('python3 setup.py sdist bdist_wheel')
os.system('python3 -m twine upload --repository pypi dist/*')
