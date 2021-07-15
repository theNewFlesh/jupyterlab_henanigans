#!/usr/bin/env python

try:
    # python2.7 doesn't have typing module
    from typing import Any, List, Tuple
except ImportError:
    pass

import argparse
import os
import re

# python2.7 doesn't have pathlib module
REPO_PATH = os.path.join(os.sep, *os.path.realpath(__file__).split(os.sep)[:-2])
REPO = os.path.split(REPO_PATH)[-1]
GITHUB_USER = 'theNewFlesh'
USER = 'ubuntu:ubuntu'
PORT = 8080
# ------------------------------------------------------------------------------

'''
A CLI for developing and deploying an app deeply integrated with this
repository's structure. Written to be python version agnostic.
'''


def get_info():
    # type: () -> Tuple[str, list]
    '''
    Parses command line call.

    Returns:
        tuple[str]: Mode and arguments.
    '''
    desc = 'A CLI for developing and deploying the {repo} app.'.format(
        repo=REPO
    )
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=desc,
        usage='\n\tpython cli.py COMMAND [-a --args]=ARGS [-h --help]'
    )

    parser.add_argument(
        'command',
        metavar='command',
        type=str,
        nargs=1,
        action='store',
        help='''Command to run in {repo} app.
    build        - Build image of {repo}
    build-prod   - Build production image of {repo}
    container    - Display the Docker container id of {repo}
    destroy      - Shutdown {repo} container and destroy its image
    destroy-prod - Shutdown {repo} production container and destroy its image
    image        - Display the Docker image id of {repo}
    lab          - Start a Jupyter lab server and build labextension
    package      - Build {repo} pip package
    prod         - Start {repo} production container
    publish      - Publish {repo} repository to python package index
    push         - Push {repo} production image to Dockerhub
    python       - Run python interpreter session inside {repo} container
    remove       - Remove {repo} Docker image
    restart      - Restart {repo} container
    requirements - Write frozen requirements to disk
    start        - Start {repo} container
    state        - State of {repo} container
    stop         - Stop {repo} container
    zsh          - Run ZSH session inside {repo} container
    zsh-complete - Generate oh-my-zsh completions
    zsh-root     - Run ZSH session as root inside {repo} container
'''.format(repo=REPO))

    parser.add_argument(
        '-a',
        '--args',
        metavar='args',
        type=str,
        nargs='+',
        action='store',
        help='Additional arguments to be passed. Be sure to include hyphen prefixes.'
    )

    temp = parser.parse_args()
    mode = temp.command[0]
    args = []
    if temp.args is not None:
        args = re.split(' +', temp.args[0])

    return mode, args


def resolve(commands):
    # type: (List[str]) -> str
    '''
    Convenience function for creating single commmand from given commands and
    resolving '{...}' substrings.

    Args:
        commands (list[str]): List of commands.

    Returns:
        str: Resolved command.
    '''
    cmd = ' && '.join(commands)

    all_ = dict(
        black='\033[0;30m',
        blue='\033[0;34m',
        clear='\033[0m',
        cyan='\033[0;36m',
        green='\033[0;32m',
        purple='\033[0;35m',
        red='\033[0;31m',
        white='\033[0;37m',
        yellow='\033[0;33m',
        github_user=GITHUB_USER,
        port=str(PORT),
        pythonpath='{PYTHONPATH}',
        repo_path=REPO_PATH,
        repo=REPO,
        user=USER,
    )
    args = {}
    for k, v in all_.items():
        if '{' + k + '}' in cmd:
            args[k] = v

    cmd = cmd.format(**args)
    return cmd


def line(text, sep=' '):
    # type: (str, str) -> str
    '''
    Convenience function for formatting a given block of text as series of
    commands.

    Args:
        text (text): Block of text.
        sep (str, optional): Line separator. Default: ' '.

    Returns:
        str: Formatted command.
    '''
    output = re.sub('^\n|\n$', '', text)  # type: Any
    output = output.split('\n')
    output = [re.sub('^ +| +$', '', x) for x in output]
    output = sep.join(output) + sep
    return output


# SUBCOMMANDS-------------------------------------------------------------------
def enter_repo():
    # type: () -> str
    '''
    Returns:
        str: Command to enter repo.
    '''
    return 'export CWD=`pwd` && cd {repo_path}'


def exit_repo():
    # type: () -> str
    '''
    Returns:
        str: Command to return to original directory.
    '''
    return 'cd $CWD'


def start():
    # type: () -> str
    '''
    Returns:
        str: Command to start container if it is not yet running.
    '''
    cmds = [
        line('''
            export STATE=`docker ps
                -a
                -f name=^{repo}$
                -f status=running
                --format='{{{{{{{{.Status}}}}}}}}'`
        '''),
        line('''
            if [ -z "$STATE" ];
                then cd docker;
                docker-compose
                    -p {repo}
                    -f {repo_path}/docker/docker-compose.yml up
                    --detach;
                cd ..;
            fi
        '''),
    ]
    return resolve(cmds)


def version_variable():
    # type: () -> str
    '''
    Returns:
        str: Command to set version variable from version.txt.
    '''
    return 'export VERSION=`cat version.txt`'


def docker_down():
    # type: () -> str
    '''
    Returns:
        str: Command to shutdown container.
    '''
    cmd = line('''
        cd docker;
        docker-compose
            -p {repo}
            -f {repo_path}/docker/docker-compose.yml
            down;
        cd ..
    ''')
    return cmd


def remove_container():
    # type: () -> str
    '''
    Returns:
        str: Command to remove container.
    '''
    return 'docker container rm --force {repo}'


def docker_exec():
    # type: () -> str
    '''
    Returns:
        str: Partial command to call 'docker exec'.
    '''
    cmd = line('''
        docker exec
            --interactive
            --tty
            --user {user}
            -e PYTHONPATH="${pythonpath}:/home/ubuntu/{repo}/python"
    ''')
    return cmd


def package_repo():
    # type: () -> str
    '''
    Returns:
        str: Command to create a temporary repo in /tmp.
    '''
    cmd = docker_exec() + line(''' {repo} zsh -c "
        cd /home/ubuntu/{repo} &&
        rm -rf /tmp/{repo} &&
        mkdir /tmp/{repo} &&
        cp docker/dev_requirements.txt /tmp/{repo}/ &&
        cp docker/prod_requirements.txt /tmp/{repo}/ &&
        cp install.json /tmp/{repo} &&
        cp LICENSE /tmp/{repo}/LICENSE &&
        cp MANIFEST.in /tmp/{repo}/MANIFEST.in &&
        cp package.json /tmp/{repo} &&
        cp pyproject.toml /tmp/{repo}/pyproject.toml &&
        cp README.md /tmp/{repo}/README.md &&
        cp RELEASE.md /tmp/{repo}/RELEASE.md &&
        cp setup.py /tmp/{repo}/ &&
        cp ts*.json /tmp/{repo} &&
        cp version.txt /tmp/{repo}/ &&
        cp -R src /tmp/{repo} &&
        cp -R style /tmp/{repo} &&
        cp -R resources /tmp/{repo}
        "
    ''')
    return cmd


# COMMANDS----------------------------------------------------------------------
def build_dev_command():
    # type: () -> str
    '''
    Returns:
        str: Command to build dev image.
    '''
    cmds = [
        enter_repo(),
        line('''
            cd docker;
            docker build
                --force-rm
                --no-cache
                --file dev.dockerfile
                --tag {repo}:latest .;
            cd ..
        '''),
        exit_repo(),
    ]
    return resolve(cmds)


def build_prod_command():
    # type: () -> str
    '''
    Returns:
        str: Command to build prod image.
    '''
    cmds = [
        enter_repo(),
        version_variable(),
        line('''
            cd docker;
            docker build
                --force-rm
                --no-cache
                --file prod.dockerfile
                --tag {github_user}/{repo}:$VERSION .;
            cd ..
        '''),
        exit_repo(),
    ]
    return resolve(cmds)


def container_id_command():
    # type: () -> str
    '''
    Returns:
        str: Command to get docker container id.
    '''
    cmds = [
        "docker ps -a --filter name=^{repo}$ --format '{{{{.ID}}}}'"
    ]
    return resolve(cmds)


def destroy_dev_command():
    # type: () -> str
    '''
    Returns:
        str: Command to destroy dev container and image.
    '''
    cmds = [
        enter_repo(),
        docker_down(),
        remove_container(),
        'docker image rm --force {repo}',
        exit_repo(),
    ]
    return resolve(cmds)


def destroy_prod_command():
    # type: () -> str
    '''
    Returns:
        str: Command to destroy prod image.
    '''
    cmds = [
        "export PROD_CID=`docker ps --filter name=^{repo}-prod$ --format '{{{{.ID}}}}'`",
        "export PROD_IID=`docker images {github_user}/{repo} --format '{{{{.ID}}}}'`",
        'docker container stop $PROD_CID',
        'docker image rm --force $PROD_IID',
    ]
    return resolve(cmds)


def image_id_command():
    # type: () -> str
    '''
    Returns:
        str: Command to get docker image id.
    '''
    cmds = [
        enter_repo(),
        start(),
        "docker images {repo} --format '{{{{.ID}}}}'",
        exit_repo(),
    ]
    return resolve(cmds)


def lab_command():
    # type: () -> str
    '''
    Returns:
        str: Command to start jupyter lab.
    '''
    cmds = [
        enter_repo(),
        start(),
        line(
            docker_exec() + '''-w /home/ubuntu/{repo} {repo} zsh -c "
                cp docker/prod_requirements.txt . &&
                cp docker/dev_requirements.txt . &&
                sudo /home/ubuntu/.local/bin/jupyter labextension develop --overwrite &&
                rm prod_requirements.txt &&
                rm dev_requirements.txt &&
                jlpm watch &
                jupyter lab --allow-root --ip=0.0.0.0 --no-browser
            "
        '''),
        exit_repo(),
    ]
    return resolve(cmds)


def package_command():
    # type: () -> str
    '''
    Returns:
        str: Command to pip package repo.
    '''
    cmds = [
        enter_repo(),
        start(),
        package_repo(),
        line(
            docker_exec() + '''{repo} zsh -c "
                cd /tmp/{repo} &&
                npm install &&
                jlpm run build &&
                python3.7 setup.py sdist
            "
        '''),
        exit_repo(),
    ]
    return resolve(cmds)


def prod_command(args):
    # type: (list) -> str
    '''
    Returns:
        str: Command to start prod container.
    '''
    if args == ['']:
        cmds = [
            line('''
                echo "Please provide a directory to map into the container
                after the {cyan}-a{clear} flag."
            ''')
        ]
        return resolve(cmds)

    run = 'docker run --volume {}:/mnt/storage'.format(args[0])
    cmds = [
        enter_repo(),
        version_variable(),
        line(run + '''
            --rm
            --publish {port}:{port}
            --name {repo}-prod
            {github_user}/{repo}:$VERSION
        '''),
        exit_repo(),
    ]
    return resolve(cmds)


def publish_command():
    # type: () -> str
    '''
    Returns:
        str: Command to publish repo as pip package.
    '''
    cmds = [
        enter_repo(),
        start(),
        package_repo(),
        docker_exec() + ' -w /tmp/{repo} {repo} python3.7 setup.py sdist',
        docker_exec() + ' -w /tmp/{repo} {repo} twine upload dist/*',
        docker_exec() + ' {repo} rm -rf /tmp/{repo}',
        exit_repo(),
    ]
    return resolve(cmds)


def push_command():
    # type: () -> str
    '''
    Returns:
        str: Command to push prod docker image to dockerhub.
    '''
    cmds = [
        enter_repo(),
        version_variable(),
        start(),
        'docker push {github_user}/{repo}:$VERSION',
        exit_repo(),
    ]
    return resolve(cmds)


def python_command():
    # type: () -> str
    '''
    Returns:
        str: Command to start python interpreter.
    '''
    cmds = [
        enter_repo(),
        start(),
        docker_exec() + ' -e REPO_ENV=True {repo} python3.7',
        exit_repo(),
    ]
    return resolve(cmds)


def remove_command():
    # type: () -> str
    '''
    Returns:
        str: Command to remove container.
    '''
    cmds = [
        enter_repo(),
        remove_container(),
        exit_repo(),
    ]
    return resolve(cmds)


def restart_command():
    # type: () -> str
    '''
    Returns:
        str: Command to restart container.
    '''
    cmds = [
        enter_repo(),
        line('''
            cd docker;
            docker-compose
                -p {repo}
                -f {repo_path}/docker/docker-compose.yml
                restart;
            cd ..
        '''),
        exit_repo(),
    ]
    return resolve(cmds)


def requirements_command():
    # type: () -> str
    '''
    Returns:
        str: Command to regenerate frozen_requirements.txt.
    '''
    cmds = [
        enter_repo(),
        start(),
        line(
            docker_exec() + '''-e REPO_ENV=True {repo} zsh -c "
                python3.7 -m pip list --format freeze >
                    /home/ubuntu/{repo}/docker/frozen_requirements.txt"
        '''),
        exit_repo(),
    ]
    return resolve(cmds)


def start_command():
    # type: () -> str
    '''
    Returns:
        str: Command to start container.
    '''
    cmds = [
        enter_repo(),
        start(),
    ]
    return resolve(cmds)


def state_command():
    # type: () -> str
    '''
    Returns:
        str: Command to get state of app.
    '''
    cmds = [
        enter_repo(),
        version_variable(),
        'export IMAGE_EXISTS=`docker images {repo} | grep -v REPOSITORY`',
        'export CONTAINER_EXISTS=`docker ps -a -f name=^{repo}$ | grep -v CONTAINER`',
        'export RUNNING=`docker ps -a -f name=^{repo}$ -f status=running | grep -v CONTAINER`',
        line(r'''
            export PORTS=`
                cat docker/docker-compose.yml |
                grep -E ' - "\d\d\d\d:\d\d\d\d"' |
                sed s'/.* - "//g' |
                sed 's/"//g' |
                sed 's/^/{blue}/g' |
                sed 's/:/{clear}-->/g' |
                awk 1 ORS=' '
            `
        '''),
        line('''
            if [ -z "$IMAGE_EXISTS" ];
                then export IMAGE_STATE="{red}absent{clear}";
            else
                export IMAGE_STATE="{green}present{clear}";
            fi;
            if [ -z "$CONTAINER_EXISTS" ];
                then export CONTAINER_STATE="{red}absent{clear}";
            elif [ -z "$RUNNING" ];
                then export CONTAINER_STATE="{red}stopped{clear}";
            else
                export CONTAINER_STATE="{green}running{clear}";
            fi
        '''),
        line('''echo
            "app: {cyan}{repo}{clear} -
            version: {yellow}$VERSION{clear} -
            image: $IMAGE_STATE -
            container: $CONTAINER_STATE -
            ports: {blue}$PORTS{clear}"
        '''),
        exit_repo(),
    ]
    return resolve(cmds)


def stop_command():
    # type: () -> str
    '''
    Returns:
        str: Command to stop container.
    '''
    cmds = [
        enter_repo(),
        docker_down(),
        exit_repo(),
    ]
    return resolve(cmds)


def zsh_command():
    # type: () -> str
    '''
    Returns:
        str: Command to run a zsh session inside container.
    '''
    cmds = [
        enter_repo(),
        start(),
        docker_exec() + ' -e REPO_ENV=True {repo} zsh',
        exit_repo(),
    ]
    return resolve(cmds)


def zsh_complete_command():
    # type: () -> str
    '''
    Returns:
        str: Command to generate and install zsh completions.
    '''
    cmds = [
        'mkdir -p ~/.oh-my-zsh/custom/completions',
        'export _COMP=~/.oh-my-zsh/custom/completions/_{repo}',
        'touch $_COMP',
        "echo 'fpath=(~/.oh-my-zsh/custom/completions $fpath)' >> ~/.zshrc",
        'echo "#compdef {repo} rec" > $_COMP',
        'echo "" >> $_COMP',
        'echo "local -a _subcommands" >> $_COMP',
        'echo "_subcommands=(" >> $_COMP',
        line('''
            bin/{repo} --help
                | grep '    - '
                | sed -E 's/ +- /:/g'
                | sed -E 's/^ +//g'
                | sed -E "s/(.*)/    '\\1'/g"
                | parallel "echo {{}} >> $_COMP"
        '''),
        'echo ")" >> $_COMP',
        'echo "" >> $_COMP',
        'echo "local expl" >> $_COMP',
        'echo "" >> $_COMP',
        'echo "_arguments \\\\" >> $_COMP',
        'echo "    \'(-h --help)\'{{-h,--help}}\'[show help message]\' \\\\" >> $_COMP',
        'echo "    \'(-d --dryrun)\'{{-d,--dryrun}}\'[print command]\' \\\\" >> $_COMP',
        'echo "    \'*:: :->subcmds\' && return 0" >> $_COMP',
        'echo "\n" >> $_COMP',
        'echo "if (( CURRENT == 1 )); then" >> $_COMP',
        'echo "    _describe -t commands \\"{repo} subcommand\\" _subcommands\" >> $_COMP',
        'echo "    return" >> $_COMP',
        'echo "fi" >> $_COMP',
    ]
    return resolve(cmds)


def zsh_root_command():
    # type: () -> str
    '''
    Returns:
        str: Command to run a zsh session as root inside container.
    '''
    return re.sub('ubuntu:ubuntu', 'root:root', zsh_command())


def get_illegal_mode_command():
    # type: () -> str
    '''
    Returns:
        str: Command to report that the mode given is illegal.
    '''
    cmds = [
        line('''
            echo "That is not a legal command.
            Please call {cyan}{repo} --help{clear} to see a list of legal
            commands."
        ''')
    ]
    return resolve(cmds)


# MAIN--------------------------------------------------------------------------
def main():
    # type: () -> None
    '''
    Print different commands to stdout depending on mode provided to command.
    '''
    mode, args = get_info()
    lut = {
        'build': build_dev_command(),
        'build-prod': build_prod_command(),
        'container': container_id_command(),
        'destroy': destroy_dev_command(),
        'destroy-prod': destroy_prod_command(),
        'image': image_id_command(),
        'lab': lab_command(),
        'package': package_command(),
        'prod': prod_command(args),
        'publish': publish_command(),
        'push': push_command(),
        'python': python_command(),
        'remove': remove_command(),
        'requirements': requirements_command(),
        'restart': restart_command(),
        'start': start_command(),
        'state': state_command(),
        'stop': stop_command(),
        'zsh': zsh_command(),
        'zsh-complete': zsh_complete_command(),
        'zsh-root': zsh_root_command(),
    }
    cmd = lut.get(mode, get_illegal_mode_command())

    # print is used instead of execute because REPO_PATH and USER do not
    # resolve in a subprocess and subprocesses do not give real time stdout.
    # So, running `command up` will give you nothing until the process ends.
    # `eval "[generated command] $@"` resolves all these issues.
    print(cmd)


if __name__ == '__main__':
    main()
