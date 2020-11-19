import re

import setuptools

with open('requirements.txt') as f:
    REQUIREMENTS = f.readlines()

with open('requirements.dev.txt') as f:
    DEV_REQUIREMENTS = f.readlines()

with open('README.md') as f:
    README = f.read()

with open('pyxivapi/__init__.py') as f:
    VERSION = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

setuptools.setup(
    name='pyxivapi',
    author='Lethys',
    author_email='seraymericbot@gmail.com',
    url='https://github.com/xivapi/xivapi-py',
    version=VERSION,
    packages=['pyxivapi'],
    license='MIT',
    description='An asynchronous Python client for XIVAPI',
    long_description=README,
    long_description_content_type="text/markdown",
    keywords='ffxiv xivapi',
    include_package_data=True,
    install_requires=REQUIREMENTS,
    extras_require={
        'dev': DEV_REQUIREMENTS,
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ]
)
