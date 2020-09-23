from setuptools import find_packages, setup
from psy
setup(
    name='sywek',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_sage=False,
    install_requires=[
        'flask',
        'gunicorn'
    ]
)
