# --repository-url https://test.pypi.org/legacy/

rm -rf build dist *.egg-info              \
   && python3 setup.py sdist bdist_wheel  \
   && python3 -m twine upload dist/*
