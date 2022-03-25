import os
import pytest


@pytest.fixture
def test_suite_dir():
    return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def test_suite_data_dir(test_suite_dir):
    return os.path.join(test_suite_dir, 'data')


@pytest.fixture
def valid_menu_design_dir(test_suite_dir):
    return os.path.join(test_suite_dir, 'data', 'correct_menu_design')


# Test click cli
@pytest.fixture
def cli_runner():
    from click.testing import CliRunner
    return CliRunner
