
import os

from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='zink',
    version='2.0.0',
    packages=['blog', 'contact', 'home', 'tweeter', 'versions'],
    include_package_data=True,
    license='MIT License',
    description='ElevenBits website.',
    long_description=README,
    url='https://elevenbits.com',
    author='Jan Willems',
    author_email='jw@elevenbits.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)