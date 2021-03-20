from click.testing import CliRunner
import pytest
import click
from pydantic import BaseSettings

from pycmdlineapp_groundwork import ConfigManager, click_config_option, with_attrs_docs



@with_attrs_docs
class RunServerSettings(BaseSettings):
    #: port number on which the server listens 
    port: int = 5555
    user: str = None

@with_attrs_docs
class Settings(BaseSettings):
    #: enable or disable application's debug mode
    debug: bool = True
    runserver: RunServerSettings = RunServerSettings()

    class Config:
        env_prefix = 'MY_APP_'
        env_file = 'tests/test.env'


test=Settings()
c = ConfigManager(model=Settings, prefix='MY_APP')
print(c.settings.dict())
print(test.dict())

@click.group(context_settings=dict(default_map=c.settings.dict() ))
@click_config_option(c)
@click.option('--debug/--no-debug', default=c.settings.debug, help=Settings.__fields__["debug"].field_info.description, type=bool, show_default=True)
@click.pass_context
def cli(ctx, debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))
    click.echo(f'Context = {ctx.default_map}')
    click.echo(f'Climate: {c.settings.dict()}')



@cli.command()
@click.option('--port', default=c.settings.runserver.port, help=RunServerSettings.__fields__["port"].field_info.description, show_default=True)
@click.option('--user', default="", prompt=True, show_default=True)
@click.pass_context
def runserver( ctx, port, user):
    click.echo(f'Serving {user} on http://127.0.0.1:{port}/' )
    click.echo(f'Context = {ctx.default_map}')
    click.echo(f'Climate: {c.settings}')


def test_hello_world():
  runner = CliRunner()
  result = runner.invoke(cli, ['--debug', 'runserver'])
  print(result.stdout)
  assert result.exit_code == 0
  pytest.fail()

if __name__ == '__main__':
    cli()

# python tests//test_climate.py --config="tests/example_cfg2.toml" --config="tests/example_cfg1.yaml" runserver
# MY_APP_RUNSERVER__PORT=2222 python tests/test_climate.py --config="tests/example_cfg2.toml" --config="tests/example_cfg1.yaml" runserver