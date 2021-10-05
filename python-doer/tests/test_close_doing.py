import os

import pytest
from click.testing import CliRunner

from pydoer.menu_creator import close_doing


runner = CliRunner()


def test_close_doing():
    response = runner.invoke(close_doing, [])
    assert response.exit_code == 0
