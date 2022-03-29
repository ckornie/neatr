from setuptools import setup, find_namespace_packages

setup(
    name='neatr',
    version='0.0.1',
    description='A bulk export for a NeatDesk database',
    long_description='NeatDesk uses an SQL Server compact database. This can be migrated to SQLite where it can then be exported.',
    author='Clancy Kornie',
    author_email='91301915+ckornie@users.noreply.github.com',
    packages=find_namespace_packages(),
    zip_safe=False,
    py_modules=[
        'neatr'
    ],
    install_requires=[
        'zstandard',
        'ocrmypdf',
        'orjson'
    ]
)