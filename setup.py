from setuptools import setup, find_packages
from notdb import __version__ as v

# README.md
with open('README.md', 'r', encoding='utf-8') as readme_file:
    readme = readme_file.read()

setup(
    name='notdb',
    packages=find_packages(),
    version=v,
    description='Viewer for NotDB Databases',
    author='Nawaf Alqari',
    author_email='nawafalqari13@gmail.com',
    keywords=['db'],
    long_description=readme,
    long_description_content_type='text/markdown',
    entry_points={
    'console_scripts': [ 'notdb=notdb.__main__:main']
    },
    project_urls={
        'Documentation': 'https://github.com/nawafalqari/NotDB_Viewer#readme',
        'Bug Tracker': 'https://github.com/nawafalqari/NotDB_Viewer/issues',
        'Source Code': 'https://github.com/nawafalqari/NotDB_Viewer/',
        'Discord': 'https://discord.gg/cpvynqk4XT'
    },
    license='MIT',
    url='https://github.com/nawafalqari/NotDB_Viewer/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)