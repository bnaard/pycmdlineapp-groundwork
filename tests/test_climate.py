import click
from climatecontrol import core, cli_utils
from click.testing import CliRunner
import pytest
from climatecontrol.ext.pydantic import Climate
from pydantic import BaseSettings, BaseModel

# settings_map = settings_parser.Climate(env_prefix='TEST_STUFF')

class RunServerSettings(BaseModel):

    port: int = 5000
    user: str = None

class Settings(BaseModel):
    debug: bool = True
    runserver: RunServerSettings = RunServerSettings()

settings = Climate(model=Settings, prefix='MY_APP')


CONTEXT_SETTINGS = dict(
    default_map=settings.settings.dict()
)


@click.group(context_settings=CONTEXT_SETTINGS)
# @click.group()
@click.option('--debug/--no-debug', help="Enable or disable debgging mode.", type=bool, show_default=True)
def cli(debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))


@cli.command()
@cli_utils.click_settings_file_option(settings)
@click.option('--port', default=settings.settings.runserver.port, show_default=True)
@click.option('--user', default="", prompt=True, show_default=True)
def runserver( port, user):
    click.echo(f'Serving {user} on http://127.0.0.1:{port}/' )


def test_hello_world():
  runner = CliRunner()
  result = runner.invoke(cli, ['--debug', 'runserver'])
  print(result.stdout)
  print(CONTEXT_SETTINGS)
  print(settings.dict())
  assert result.exit_code == 0
  pytest.fail()

if __name__ == '__main__':
    cli()