import click
import os
import subprocess
import go_prog
import java_prog
import play_prog
import topic_creator
import util

pidfile = "/var/tmp/ons_sm.pid"
java_progs = ['dp-dd-dimensional-metadata-api', 'dp-dd-metadata-editor', 'dp-dd-request-filter']
play_progs = ['dp-dd-database-loader']
go_progs = ['dp-csv-splitter', 'dp-dd-csv-filter', 'dp-dd-csv-transformer', 'dp-dd-file-uploader',
            'dp-dd-frontend-controller', 'dp-frontend-renderer']
all_progs = java_progs + play_progs + go_progs

kafka_topics = ['dataset-status', 'dead-dataset', 'file-uploaded', 'filter-request', 'test', 'transform-request']

@click.command()
@click.option('--install', '-i', is_flag=True, help='Greet as a cowboy.')
@click.option('--check', '-c', is_flag=True, help='Perform a check before running command')
@click.option('--list-topics', '-lt', is_flag=True, help='List all kafka topics')
def main(install, check, list_topics):
    """A set of scripts for launching servies and kafka queues """
    if check:
        check_system()
    elif install:
        check_system()
        install_programs()
        click.echo('I\'m installing something, I promise')


    if (list_topics):
        list_all_topics()

def list_all_topics():
    command = '{0} --list --zookeeper {1}'.format(util.kafka_topic_command(), util.zoo_keeper_addr())
    util.execute_command_and_exit_if_failure(command)

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
    for topic in kafka_topics:
        zookeeper_addr = util.zoo_keeper_addr()
        topic_creator.create_topic(topic, zookeeper_addr, 1, 1)

def check_system():
    click.echo("Checking for pre-requisites")
    sp = subprocess.Popen(["java", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    java_version = sp.communicate()
    java_home = os.environ.get('JAVA_HOME')
    go_path = os.environ.get('GOPATH')
    go_root = os.environ.get('GOROOT')
    java_dir = os.environ.get('JAVA_WORKSPACE')
    zookeeper_addr = os.environ.get('ZOOKEEPER')
    kafka_addr = os.environ.get('KAFKA_ADDR')
    success = sp.wait()
    if success != 0 or '1.8' not in ''.join(java_version):
        click.echo("Java 8 must be installed in the system")
        exit(1)

    elif not java_home:
        click.echo("JAVA_HOME environment variable must be set")

    elif not util.which('go'):
        click.echo("Golang must be installed")

    elif not util.which('git'):
        click.echo('GIT version control system system must be installed')

    elif not go_path:
        click.echo("GOPATH environment variable must be set")


    elif not java_dir:
        click.echo('JAVA_WORKSPACE has not been set. Please set this environment variable')

    elif not util.which('mvn'):
        click.echo("Maven is not installed, please install maven and have it in your binary path.")
        exit(1)

    elif not util.which('sbt'):
        click.echo("SBT is not installed, please install sbt and have it in your binary path.")
        exit(1)

    elif not util.which('javac'):
        click.echo("javac is not installed or is not in your, please make sure it's available for maven")
        exit(1)

    else:
        click.echo('Java found at %s' % util.which('java'))
        click.echo('JAVA_HOME found %s' % java_home)
        click.echo('JAVA_WORKSPACE has been set to %s' % java_dir)
        click.echo('GOPATH set to %s' % go_path)
        if go_root: click.echo('GOROOT set to %s' % go_root)
        click.echo('GIT found at %s' % util.which('git'))
        click.echo('Prerequisites successfully found')
        if kafka_addr and len(kafka_addr) > 0:
            click.echo('KAFKA_ADDR set to %s' % kafka_addr)
        else:
            click.echo('KAFKA_ADDR not set, using localhost:9092')
        if zookeeper_addr and len(zookeeper_addr) > 0:
            click.echo('ZOOKEEPER set to %s' % zookeeper_addr)
        else:
            click.echo('ZOOKEEPER not set, using localhost:2181')




