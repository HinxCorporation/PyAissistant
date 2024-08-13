Remove-Item build -Recurse
Remove-Item dist -Recurse
Remove-Item *.egg-info -Recurse
python setup.py sdist bdist_wheel
