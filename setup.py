
from setuptools import setup

setup(
    version='0.0.2',
    name='nivad',
    description='Nivad server-server api package',
    url='https://github.com/NivadCloud/NivadPy',
    author='MJafar Mashhadi',
    author_email='mjafar@nivad.io',
    license='GPL',
    packages=['nivad'],
    install_requires=[
        'urllib3',
        'PyJWT',
        'certifi'
    ],
    zip_safe=False
)
