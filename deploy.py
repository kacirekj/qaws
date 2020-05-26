import os

os.system(f'git commit')
os.system('python3 setup.py sdist bdist_wheel')
os.system('python3 -m twine upload --repository pypi dist/*')
