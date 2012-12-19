import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
path, script = os.path.split(sys.argv[0])
os.chdir(os.path.abspath(path))

install_requires = [
    'Flask==0.9',
    'Flask-Admin==1.0.3',
    'Flask-DebugToolbar==0.7.1',
    'Flask-OAuth==0.12',
    'Flask-SQLAlchemy==0.16',
    'Flask-WTF==0.8',
    'Jinja2==2.6',
    'SQLAlchemy==0.7.9',
    'WTForms==1.0.2',
    'Werkzeug==0.8.3',
    'argparse==1.2.1',
    'blinker==1.2',
    'httplib2==0.7.7',
    'oauth2==1.5.211',
    'wsgiref==0.1.2',
]

setup(name='biffy',
    version="0.0.1",
    description='Biffy: The Batteries-Included Flask-based Framework',
    author='Andrew Sledge',
    author_email='andrew.j.sledge@gmail.com',
    url='http://sledge.io/',
    install_requires=install_requires,
    test_suite='test',
)