import click
import subprocess
import os

def execute_command_and_exit_if_failure(cmd, directory=os.path.dirname(os.path.realpath(__file__))):
    click.echo()
    click.echo('<*****************************************************************************>')
    click.echo('executing the following command:')
    click.echo(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=directory)

    # Poll process for new output until finished
    while True:
        next_line = process.stdout.readline()
        if next_line == '' and process.poll() is not None:
            break
        stripped_line = next_line.rstrip()
        if len(stripped_line) > 0: click.echo(stripped_line)

    output = process.communicate()[0]
    exitCode = process.returncode

    if (exitCode == 0):
        return output
    else:
        click.echo("Error in executing last command, aborting with status code 1")
        exit(1)

# We want this for go get as it will always fail if there is no "buildable" source
def execute_command_and_ignore_failure(cmd, directory=os.path.dirname(os.path.realpath(__file__))):
    click.echo()
    click.echo('<*****************************************************************************>')
    click.echo('executing the following command:')
    click.echo(cmd)
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=directory)

    # Poll process for new output until finished
    while True:
        next_line = process.stdout.readline()
        if next_line == '' and process.poll() is not None:
            break
        stripped_line = next_line.rstrip()
        if len(stripped_line) > 0: click.echo(stripped_line)

    return process.communicate()[0]

def git_url_for(prog_name):
    return 'git@github.com:ONSdigital/%s.git' % prog_name

def go_get_url(prog_name):
    return 'github.com/ONSdigital/%s' % prog_name

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

def zoo_keeper_addr():
    address = os.environ.get('ZOOKEEPER')
    if address and len(address) > 0:
        return address
    else:
        return 'localhost:2181'

def kafka_topic_command():
    command = 'kafka-topics'
    command_sh = '%s.sh' % command
    if which(command):
        return command
    elif which(command_sh):
        return command_sh
    else:
        click.echo("Could not find {0} or {1}. Please make sure the kafka utils are installed and are on your PATH".
                   format(command, command_sh))

def check_if_topic_exists(topic, zookeeper_addr):
    ktc = kafka_topic_command()
    command = '{0} --list --zookeeper {1}'.format(ktc, zookeeper_addr)
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output = proc.communicate()
    proc.wait()
    for o in output:
        if o and topic in o.split():
            return True

    return False
