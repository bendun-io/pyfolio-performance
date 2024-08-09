python setup.py sdist bdist_wheel
twine check dist/*
pip install --force-reinstall dist/pyfolio_performance-0.2.1-py3-none-any.whl