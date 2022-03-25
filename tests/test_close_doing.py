from click.testing import CliRunner

from pydoer.cli import close_doing


runner = CliRunner()


def test_close_doing():
    response = runner.invoke(close_doing, [])
    assert response.exit_code == 0
