from setuptools import find_packages, setup


with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='Percepto',
    version='1.0.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    package_data={
        "cfg.cfg_global": ["*.json"],
        "cfg.cfg_tests": ["*.json"]
    },
    author='efi ovadia',
    author_email='efovadia@gmail.com',
    description='Percepto Assignment',
    license='',
    install_requires=[required, 'pytest']
)
