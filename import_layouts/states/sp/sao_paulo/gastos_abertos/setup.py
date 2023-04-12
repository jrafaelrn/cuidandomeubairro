# -*- coding: utf-8 -*-

from setuptools import setup

project = "gastosabertos"

setup(
    name=project,
    version='0.0.1',
    url='https://github.com/okfn-brasil/gastos_abertos',
    description='Visualization of public spending in Sao Paulo city for Gastos Abertos project',
    author='Edgar Zanella Alvarenga',
    author_email='e@vaz.io',
    packages=["gastosabertos"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask==0.10.1',
        'Flask-SQLAlchemy==2.1',
        'Flask-WTF==0.13.1',
        'Flask-Script==2.0.5',
        'Flask-Babel==0.11.1',
        'Flask-Testing==0.6.2',
        'Flask-Restful==0.3.5',
        'Flask-Paginate==0.5.0',
        'Flask-CORS>=2.0.1',
        'Flask-Restplus==0.10.4',
        'geoalchemy2==0.4.0',
        'fabric==1.10.2',
        'docopt==0.6.2',
        'pandas==0.18.1',
        'geopy==1.11.0',
        'shapely==1.5.17',
        'psycopg2==2.6.2',
        'xlrd==1.0.0',
        'elasticsearch==1.0.0',
        'elasticsearch-dsl==2.0.0',
	    'futures==3.0.5',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries'
    ]
)
