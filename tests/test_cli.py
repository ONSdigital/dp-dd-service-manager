import pytest
from click.testing import CliRunner
from onsdigital import cli
from onsdigital import util


@pytest.fixture
def runner():
    return CliRunner()


# def test_cli(runner):
#     result = runner.invoke(cli.main)
#     assert result.exit_code == 0
#     assert not result.exception
#     assert result.output.strip() == 'Hello, world.'
#
#
# def test_cli_with_option(runner):
#     result = runner.invoke(cli.main, ['--as-cowboy'])
#     assert not result.exception
#     assert result.exit_code == 0
#     assert result.output.strip() == 'Howdy, world.'
#
#
# def test_cli_with_arg(runner):
#     result = runner.invoke(cli.main, ['ONS'])
#     assert result.exit_code == 0
#     assert not result.exception
#     assert result.output.strip() == 'Hello, ONS.'

def test_git_url():
    assert util.git_url_for("dp") == 'git@github.com:ONSdigital/dp.git'

def test_go_get_url():
    assert util.go_get_url("dp-dd-dataset-importer") == 'github.com/ONSdigital/dp-dd-dataset-importer'