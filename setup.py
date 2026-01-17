from setuptools import setup, find_packages

setup(
    name='pystickynote',
    version='2.0.0',
    author='Max Bridgland',
    author_email='mabridgland@protonmail.com',
    description='Easy Sticky Note Widgets',
    long_description=open('README.md', 'r').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/M4cs/pystickynote',
    packages=find_packages(),
    python_requires='>=3.7',
    install_requires=[
        'customtkinter>=5.0.0',
    ],
    project_urls={
        'Discord Server': 'https://discordapp.com/invite/7VN9VZe'
    },
    license='GNU General Public License v3 (GPLv3) (GPL)',
    zip_safe=True,
    entry_points={
        'console_scripts':[
            'pystickynote = pystickynote.__main__:main',
            'pysn = pystickynote.__main__:main'
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',

        'Programming Language :: Python :: Implementation :: CPython',

        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',

        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities',
    ]
)