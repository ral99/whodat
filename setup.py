from setuptools import setup

setup(
    name='whodat',
    version='0.1',
    packages=['whodat'],
    package_dir={'': 'src'},
    install_requires=['WebOb==1.5.0'],
    author='Rodrigo A. Lima',
    description='A lightweight web framework that encourages clean design.',
    license='BSD',
    keywords='wsgi web',
)
