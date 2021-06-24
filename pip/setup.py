from setuptools import setup, find_packages

with open('version.txt') as f:
    VERSION = f.read().strip('\n')

with open('prod_requirements.txt') as f:
    PROD_REQUIREMENTS = f.read().split('\n')

with open('dev_requirements.txt') as f:
    DEV_REQUIREMENTS = f.read().split('\n')

with open('README.md') as f:
    README = f.read()
# ------------------------------------------------------------------------------

setup(
    name='jupyterlab_henanigans',
    packages=find_packages(where='./', exclude=['.*test.*.py', '.*.pyc']),
    package_dir={'jupyterlab_henanigans': 'jupyterlab_henanigans'},
    include_package_data=True,
    version=VERSION,
    license='MIT',
    description='Henanigans theme for JupyterLab.',
    long_description=README,
    long_description_content_type='text/markdown',
    author='Aex Braun',
    author_email='alexander.g.braun@gmail.com',
    url='https://github.com/theNewFlesh/jupyterlab_henanigans',
    download_url='https://github.com/theNewFlesh/jupyterlab_henanigans/archive/' + VERSION + '.tar.gz',
    keywords=['jupyter', 'jupyterlab', 'theme', 'henanigans'],
    install_requires=PROD_REQUIREMENTS,
    classifiers=[
      'Development Status :: 4 - Beta',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: MIT License',
      'Programming Language :: Python :: 3',
      'Programming Language :: Python :: 3.7',
    ],
    extras_require={
        "dev": DEV_REQUIREMENTS
    },
)
