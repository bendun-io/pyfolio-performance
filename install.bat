python setup.py sdist bdist_wheel
twine check dist/*
pip install dist/pyfolio_performance-0.1.1-py3-none-any.whl