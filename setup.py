import os
import io
import re

from setuptools import setup, find_packages


cwd = os.path.abspath(os.path.dirname(__file__))


def read(*names, **kwargs):
    with io.open(
        os.path.join(cwd, *names), encoding=kwargs.get('encoding', 'utf8')
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]',
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError('Unable to find version string.')


def md_to_rst(text):
    try:
        import pypandoc
    except ImportError:
        pass
    else:
        text = pypandoc.convert_text(text, 'rst', 'markdown_github')
    return text


classifiers = [
    #   3 - Alpha
    #   4 - Beta
    #   5 - Production/Stable
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
]

setup(
    name='wt',
    version=find_version('wt', '__init__.py'),
    description='Static blog generator',
    long_description=md_to_rst(read('README.md')),
    url='https://github.com/ysegorov/wt',
    author='Yuri Egorov',
    author_email='ysegorov@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='blog static site generator',
    packages=find_packages(exclude=['tests']),
    package_data={
        'wt': ['templates/*.html', 'templates/*.xml', 'templates/*.yaml']},
    install_requires=[
        'markdown>=2.6.6',
        'jinja2>=2.8',
        'pyyaml>=3.12',
        'aiohttp~=0.22.5',
        'cached-property>=1.3.0',
    ],
    extras_require={
        'dev': [
            'twine>=1.8.1',
            'coverage>=4.2',
            'pytest>=3.0.0',
            'pytest-cov>=2.3.1',
            'pytest-catchlog>=1.2.2',
            'pytest-aiohttp>=0.1.3',
        ]
    },
    setup_requires=['pytest-runner>=2.0,<3dev'],
    tests_require=['pytest>=3.0.0',
                   'pytest-catchlog>=1.2.2',
                   'pytest-aiohttp>=0.1.3'],
    entry_points={
        'console_scripts': [
            'wt=wt.cli:main'
        ]
    }
)
