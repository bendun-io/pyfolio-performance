python setup.py sdist bdist_wheel
twine check dist/*
pip install --force-reinstall dist/pyfolio_performance-0.1.7-py3-none-any.whl