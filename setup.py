from setuptools import setup, find_packages
import codecs
import os.path

# got these 2 functions from https://packaging.python.org/en/latest/guides/single-sourcing-package-version/
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

# README.md
with open('README.md', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

setup(
    name='notdb',
    packages=find_packages(),
    install_requires=[
        'pyonr>=1.0.0',
        'bcrypt>=3.2.0'
    ],
    version=get_version('notdb/__init__.py'),
    description='NotDB is a PYON-like database',
    author='Nawaf Alqari',
    author_email='nawafalqari13@gmail.com',
    keywords=['notdb', 'db', 'database', 'notdatabsae', 'simple database'],
    long_description=readme,
    long_description_content_type='text/markdown',
    entry_points={
        'console_scripts': ['notdb=notdb.__main__:main']
    },
    license='MIT',
    zip_safe=False,
    url='https://github.com/nawafalqari/NotDB/',
    project_urls={
        'Documentation': 'https://github.com/nawafalqari/NotDB#readme',
        'Bug Tracker': 'https://github.com/nawafalqari/NotDB/issues',
        'Source Code': 'https://github.com/nawafalqari/NotDB/',
        'Discord': 'https://discord.gg/cpvynqk4XT'
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Database'
    ],
)