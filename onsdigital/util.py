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