import click
import os
import subprocess
import go_prog
import java_prog
import play_prog

pidfile = "/var/tmp/ons_sm.pid"
java_progs = ['dp-dd-dimensional-metadata-api', 'dp-dd-metadata-editor', 'dp-dd-request-filter']
play_progs = ['dp-dd-database-loader']
go_progs = ['dp-csv-splitter', 'dp-dd-csv-filter', 'dp-dd-csv-transformer', 'dp-dd-file-uploader',
            'dp-dd-frontend-controller', 'dp-frontend-renderer']
all_progs = java_progs + play_progs + go_progs

@click.command()
@click.option('--install', '-i', is_flag=True, help='Greet as a cowboy.')
@click.option('--check', '-c', is_flag=True, help='Perform a check before running command')
def main(install, check):
    """A set of scripts for launching servies and kafka queues """
    if check:
        check_system()
    elif install:
        check_system()
        install_programs()
        click.echo('I\'m installing something, I promise')
    else:
        click.echo('{0}, {1}.'.format('Hello', 'Mo'))

def list_program(prog_name):
    click.echo('Listing all program running and their pids')

def stop_program(prog_name):
    click.echo('I promise to stop this prog')


def install_programs():
    for gopher in go_progs:
        go_prog.install(gopher)
    for j in java_progs:
        java_prog.install(j)
    for p in play_progs:
        play_prog.install(p)
    click.echo('I promise to stop this prog')

def check_system():
    click.echo("Checking for pre-requisites")
    sp = subprocess.Popen(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    java_version = sp.communicate()
    java_home = os.environ.get('JAVA_HOME')
    go_path = os.environ.get('GOPATH')
    go_root = os.environ.get('GOROOT')
    java_dir = os.environ.get('JAVA_WORKSPACE')
    success = sp.wait()
    if success != 0 or '1.8' not in ''.join(java_version):
        click.echo("Java 8 must be installed in the system")
        exit(1)

    elif not java_home:
        click.echo("JAVA_HOME environment variable must be set")

    elif not which('go'):
        click.echo("Golang must be installed")

    elif not which('git'):
        click.echo('GIT version control system system must be installed')

    elif not go_path:
        click.echo("GOPATH environment variable must be set")


    elif not java_dir:
        click.echo('JAVA_WORKSPACE has not been set. Please set this environment variable')

    else:
        click.echo('Java found at %s' % which('java'))
        click.echo('JAVA_HOME found %s' % java_home)
        click.echo('JAVA_WORKSPACE has been set to %s' % java_dir)
        click.echo('GOPATH set to %s' % go_path)
        if go_root: click.echo('GOROOT set to %s' % go_root)
        click.echo('GIT found at %s' % which('git'))
        click.echo('Prerequisites successfully found')

def which(program):
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            path = path.strip('"')
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None


