import json
from pathlib import Path

import setuptools

with open('version.txt') as f:
    VERSION = f.read().strip('\n')

with open('prod_requirements.txt') as f:
    PROD_REQUIREMENTS = f.read().split('\n')

with open('dev_requirements.txt') as f:
    DEV_REQUIREMENTS = f.read().split('\n')

with open('README.md') as f:
    README = f.read()
# ------------------------------------------------------------------------------

HERE = Path(__file__).parent.resolve()

# The name of the project
name = "jupyterlab_henanigans"

lab_path = (HERE / name.replace("-", "_") / "labextension")

# Representative files that should exist after a successful build
ensured_targets = [
    str(lab_path / "package.json"),
    str(lab_path / "static/style.js")
]

labext_name = "@theNewFlesh/jupyterlab_henanigans"

data_files_spec = [
    ("share/jupyter/labextensions/%s" % labext_name, str(lab_path), "**"),
    ("share/jupyter/labextensions/%s" % labext_name, str(HERE), "install.json"),
]

# Get the package info from package.json
pkg_json = json.loads((HERE / "package.json").read_bytes())

setup_args = dict(
    name=name,
    version=VERSION,
    url=pkg_json["homepage"],
    author=pkg_json["author"]["name"],
    author_email=pkg_json["author"]["email"],
    description=pkg_json["description"],
    download_url='https://github.com/theNewFlesh/jupyterlab_henanigans/archive/' + VERSION + '.tar.gz',
    license=pkg_json["license"],
    long_description=README,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=PROD_REQUIREMENTS,
    extras_require={"dev": DEV_REQUIREMENTS},
    zip_safe=False,
    include_package_data=True,
    python_requires=">=3.6",
    platforms="Linux, Mac OS X, Windows",
    keywords=['jupyter', 'jupyterlab', 'theme', 'henanigans'],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Framework :: Jupyter",
    ],
)

try:
    from jupyter_packaging import (
        wrap_installers,
        npm_builder,
        get_data_files
    )
    post_develop = npm_builder(
        build_cmd="install:extension", source_dir="src", build_dir=lab_path
    )
    setup_args['cmdclass'] = wrap_installers(
        post_develop=post_develop, ensured_targets=ensured_targets
    )
    setup_args['data_files'] = get_data_files(data_files_spec)
except ImportError as e:
    pass

if __name__ == "__main__":
    setuptools.setup(**setup_args)
