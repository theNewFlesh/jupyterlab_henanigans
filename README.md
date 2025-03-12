<p>
    <a href="https://www.linkedin.com/in/alexandergbraun" rel="nofollow noreferrer">
        <img src="https://www.gomezaparicio.com/wp-content/uploads/2012/03/linkedin-logo-1-150x150.png"
             alt="linkedin" width="30px" height="30px"
        >
    </a>
    <a href="https://github.com/theNewFlesh" rel="nofollow noreferrer">
        <img src="https://tadeuzagallo.com/GithubPulse/assets/img/app-icon-github.png"
             alt="github" width="30px" height="30px"
        >
    </a>
    <a href="https://pypi.org/user/the-new-flesh" rel="nofollow noreferrer">
        <img src="https://cdn.iconscout.com/icon/free/png-256/python-2-226051.png"
             alt="pypi" width="30px" height="30px"
        >
    </a>
    <a href="http://vimeo.com/user3965452" rel="nofollow noreferrer">
        <img src="https://cdn1.iconfinder.com/data/icons/somacro___dpi_social_media_icons_by_vervex-dfjq/500/vimeo.png"
             alt="vimeo" width="30px" height="30px"
        >
    </a>
    <a href="https://alexgbraun.com" rel="nofollow noreferrer">
        <img src="https://i.ibb.co/fvyMkpM/logo.png"
             alt="alexgbraun" width="30px" height="30px"
        >
    </a>
</p>

<!-- <img id="logo" src="resources/logo.png" style="max-width: 717px"> -->

[![](https://img.shields.io/badge/License-MIT-F77E70?style=for-the-badge)](https://github.com/theNewFlesh/jupyterlab_henanigans/blob/master/LICENSE)
[![](https://img.shields.io/pypi/pyversions/jupyterlab_henanigans?style=for-the-badge&label=Python&color=A0D17B&logo=python&logoColor=A0D17B)](https://github.com/theNewFlesh/jupyterlab_henanigans/blob/master/docker/config/pyproject.toml)
[![](https://img.shields.io/pypi/v/jupyterlab_henanigans?style=for-the-badge&label=PyPI&color=5F95DE&logo=pypi&logoColor=5F95DE)](https://pypi.org/project/jupyterlab_henanigans/)
[![](https://img.shields.io/pypi/dm/jupyterlab_henanigans?style=for-the-badge&label=Downloads&color=5F95DE)](https://pepy.tech/project/jupyterlab_henanigans)

# Introduction

Henanigans theme for Jupyter Lab.

<img src='resources/screenshot.png' width='800px'>

See [documentation](https://theNewFlesh.github.io/jupyterlab_henanigans/) for details.

# Installation for Developers

### Docker
1. Install [docker-desktop](https://docs.docker.com/desktop/)
2. Ensure docker-desktop has at least 4 GB of memory allocated to it.
3. `git clone git@github.com:theNewFlesh/jupyterlab_henanigans.git`
4. `cd jupyterlab_henanigans`
5. `chmod +x bin/jupyterlab_henanigans`
6. `bin/jupyterlab_henanigans docker-start`
   - If building on a M1 Mac run `export DOCKER_DEFAULT_PLATFORM=linux/amd64` first.

The service should take a few minutes to start up.

Run `bin/jupyterlab_henanigans --help` for more help on the command line tool.

### Extension Build

Note: You will need NodeJS to build the extension package.

The `jlpm` command is JupyterLab's pinned version of
[yarn](https://yarnpkg.com/) that is installed with JupyterLab. You may use
`yarn` or `npm` in lieu of `jlpm` below.

```bash
# Clone the repo to your local environment
# Change directory to the jupyterlab_henanigans directory
# Install package in development mode
pip install -e .
# Link your development version of the extension with JupyterLab
jupyter labextension develop . --overwrite
# Rebuild extension Typescript source after making changes
jlpm run build
```

You can watch the source directory and run JupyterLab at the same time in different terminals to watch for changes in the extension's source and automatically rebuild the extension.

```bash
# Watch the source directory in one terminal, automatically rebuilding when needed
jlpm run watch
# Run JupyterLab in another terminal
jupyter lab
```

With the watch command running, every saved change will immediately be built locally and available in your running JupyterLab. Refresh JupyterLab to load the change in your browser (you may need to wait several seconds for the extension to be rebuilt).

By default, the `jlpm run build` command generates the source maps for this extension to make it easier to debug using the browser dev tools. To also generate source maps for the JupyterLab core extensions, you can run the following command:

```bash
jupyter lab build --minimize=False
```

### Development uninstall

```bash
pip uninstall jupyterlab_henanigans
```

In development mode, you will also need to remove the symlink created by `jupyter labextension develop`
command. To find its location, you can run `jupyter labextension list` to figure out where the `labextensions`
folder is located. Then you can remove the symlink named `@theNewFlesh/jupyterlab_henanigans` within that folder.

### ZSH Setup
1. `bin/jupyterlab_henanigans` must be run from this repository's top level directory.
2. Therefore, if using zsh, it is recommended that you paste the following line
    in your ~/.zshrc file:
    - `alias jupyterlab_henanigans="cd [parent dir]/jupyterlab_henanigans; bin/jupyterlab_henanigans"`
    - Replace `[parent dir]` with the parent directory of this repository
3. Consider adding the following line to your ~/.zshrc if you are using a M1 Mac:
    - `export DOCKER_DEFAULT_PLATFORM=linux/amd64`
4. Running the `zsh-complete` command will enable tab completions of the cli
   commands, in the next shell session.

   For example:
   - `jupyterlab_henanigans [tab]` will show you all the cli options, which you can press
     tab to cycle through
   - `jupyterlab_henanigans docker-[tab]` will show you only the cli options that begin with
     "docker-"

# Installation for Production

### Python
`pip install jupyterlab_henanigans`

### Docker
1. Install [docker-desktop](https://docs.docker.com/desktop/)
2. `docker pull theNewFlesh/jupyterlab_henanigans:[mode]-[version]`


---

# Quickstart Guide
This repository contains a suite commands for the whole development process.
This includes everything from testing, to documentation generation and
publishing pip packages.

These commands can be accessed through:

  - The VSCode task runner
  - The VSCode task runner side bar
  - A terminal running on the host OS
  - A terminal within this repositories docker container

Running the `zsh-complete` command will enable tab completions of the CLI.
See the zsh setup section for more information.

### Command Groups

Development commands are grouped by one of 10 prefixes:

| Command    | Description                                                                        |
| ---------- | ---------------------------------------------------------------------------------- |
| build      | Commands for building packages for testing and pip publishing                      |
| docker     | Common docker commands such as build, start and stop                               |
| docs       | Commands for generating documentation and code metrics                             |
| library    | Commands for managing python package dependencies                                  |
| session    | Commands for starting interactive sessions such as jupyter lab and python          |
| state      | Command to display the current state of the repo and container                     |
| test       | Commands for running tests, linter and type annotations                            |
| version    | Commands for bumping project versions                                              |
| quickstart | Display this quickstart guide                                                      |
| zsh        | Commands for running a zsh session in the container and generating zsh completions |

### Common Commands

Here are some frequently used commands to get you started:

| Command           | Description                                               |
| ----------------- | --------------------------------------------------------- |
| docker-restart    | Restart container                                         |
| docker-start      | Start container                                           |
| docker-stop       | Stop container                                            |
| docs-full         | Generate documentation, coverage report, diagram and code |
| library-add       | Add a given package to a given dependency group           |
| library-graph-dev | Graph dependencies in dev environment                     |
| library-remove    | Remove a given package from a given dependency group      |
| library-search    | Search for pip packages                                   |
| library-update    | Update dev dependencies                                   |
| session-lab       | Run jupyter lab server                                    |
| state             | State of                                                  |
| test-dev          | Run all tests                                             |
| test-lint         | Run linting and type checking                             |
| zsh               | Run ZSH session inside container                          |
| zsh-complete      | Generate ZSH completion script                            |

---

# Development CLI
bin/jupyterlab_henanigans is a command line interface (defined in cli.py) that
works with any version of python 2.7 and above, as it has no dependencies.
Commands generally do not expect any arguments or flags.

Its usage pattern is: `bin/jupyterlab_henanigans COMMAND [-a --args]=ARGS [-h --help] [--dryrun]`

### Commands
The following is a complete list of all available development commands:

| Command                    | Description                                                         |
| -------------------------- | ------------------------------------------------------------------- |
| build-edit-prod-dockerfile | Edit prod.dockefile to use local package                            |
| build-local-package        | Generate local pip package in docker/dist                           |
| build-package              | Build production version of repo for publishing                     |
| build-prod                 | Publish pip package of repo to PyPi                                 |
| build-publish              | Run production tests first then publish pip package of repo to PyPi |
| build-test                 | Build test version of repo for prod testing                         |
| docker-build               | Build development image                                             |
| docker-build-from-cache    | Build development image from registry cache                         |
| docker-build-no-cache      | Build development image without cache                               |
| docker-build-prod          | Build production image                                              |
| docker-build-prod-no-cache | Build production image without cache                                |
| docker-container           | Display the Docker container id                                     |
| docker-destroy             | Shutdown container and destroy its image                            |
| docker-destroy-prod        | Shutdown production container and destroy its image                 |
| docker-image               | Display the Docker image id                                         |
| docker-prod                | Start production container                                          |
| docker-pull-dev            | Pull development image from Docker registry                         |
| docker-pull-prod           | Pull production image from Docker registry                          |
| docker-push-dev            | Push development image to Docker registry                           |
| docker-push-dev-latest     | Push development image to Docker registry with dev-latest tag       |
| docker-push-prod           | Push production image to Docker registry                            |
| docker-push-prod-latest    | Push production image to Docker registry with prod-latest tag       |
| docker-remove              | Remove Docker image                                                 |
| docker-restart             | Restart container                                                   |
| docker-start               | Start container                                                     |
| docker-stop                | Stop container                                                      |
| docs                       | Generate sphinx documentation                                       |
| docs-architecture          | Generate architecture.svg diagram from all import statements        |
| docs-full                  | Generate documentation, coverage report, diagram and code           |
| docs-metrics               | Generate code metrics report, plots and tables                      |
| library-add                | Add a given package to a given dependency group                     |
| library-graph-dev          | Graph dependencies in dev environment                               |
| library-graph-prod         | Graph dependencies in prod environment                              |
| library-install-dev        | Install all dependencies into dev environment                       |
| library-install-prod       | Install all dependencies into prod environment                      |
| library-list-dev           | List packages in dev environment                                    |
| library-list-prod          | List packages in prod environment                                   |
| library-lock-dev           | Resolve dev.lock file                                               |
| library-lock-prod          | Resolve prod.lock file                                              |
| library-remove             | Remove a given package from a given dependency group                |
| library-search             | Search for pip packages                                             |
| library-sync-dev           | Sync dev environment with packages listed in dev.lock               |
| library-sync-prod          | Sync prod environment with packages listed in prod.lock             |
| library-update             | Update dev dependencies                                             |
| library-update-pdm         | Update PDM                                                          |
| quickstart                 | Display quickstart guide                                            |
| session-lab                | Run jupyter lab server                                              |
| session-python             | Run python session with dev dependencies                            |
| state                      | State of repository and Docker container                            |
| test-coverage              | Generate test coverage report                                       |
| test-dev                   | Run all tests                                                       |
| test-fast                  | Test all code excepts tests marked with SKIP_SLOWS_TESTS decorator  |
| test-format                | Format all python files                                             |
| test-lint                  | Run linting and type checking                                       |
| test-prod                  | Run tests across all support python versions                        |
| version                    | Full resolution of repo: dependencies, linting, tests, docs, etc    |
| version-bump-major         | Bump pyproject major version                                        |
| version-bump-minor         | Bump pyproject minor version                                        |
| version-bump-patch         | Bump pyproject patch version                                        |
| version-commit             | Tag with version and commit changes to master                       |
| zsh                        | Run ZSH session inside Docker container                             |
| zsh-complete               | Generate oh-my-zsh completions                                      |
| zsh-root                   | Run ZSH session as root inside Docker container                     |

### Flags

| Short | Long      | Description                                          |
| ----- | --------- | ---------------------------------------------------- |
| -a    | --args    | Additional arguments, this can generally be ignored  |
| -h    | --help    | Prints command help message to stdout                |
|       | --dryrun  | Prints command that would otherwise be run to stdout |


