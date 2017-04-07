import util
import os
import click

def install(prog_name):
    git_url = util.git_url_for(prog_name)
    java_dir = os.environ.get('JAVA_WORKSPACE')
    if not java_dir:
        click.echo('Make sure $JAVA_WORKSPACE env parameter is set')
    project_dir = '{0}/{1}'.format(java_dir, prog_name)
    util.execute_command_and_ignore_failure('git clone %s' % git_url, java_dir) # fails if project already exists
    util.execute_command_and_exit_if_failure('git fetch origin', project_dir)
    util.execute_command_and_exit_if_failure('git checkout origin/develop', project_dir)
    util.execute_command_and_exit_if_failure('mvn clean compile', project_dir)