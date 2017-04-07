import util
import os
import click

def zoo_keeper_addr():
    address = os.environ.get('ZOOKEEPER')
    if address and len(address) > 0:
        return address
    else:
        return 'localhost:2181'

def create_topic(topic, zookeeper_addr, partition_num, replication_factor):
    if util.check_if_topic_exists(topic, zookeeper_addr):
        click.echo('%s topic already exists in zookeeper' % topic)
    else:
        util.execute_command_and_exit_if_failure(create_kafka_command(topic,
                                                                      zookeeper_addr,
                                                                      partition_num,
                                                                      replication_factor))

def create_kafka_command(topic, zookeeper_addr, partition_num, replication_factor):
    kafka_command = util.kafka_topic_command()
    return "{0} --create --zookeeper {1} --replication-factor {2} --partitions {3} --topic {4}".\
        format(kafka_command, zookeeper_addr, replication_factor, partition_num, topic)

