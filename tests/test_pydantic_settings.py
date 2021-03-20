from click.testing import CliRunner
import pytest
import click
from pydantic import BaseModel, BaseSettings

# from pycmdlineapp_groundwork import ConfigManager, click_config_option
from pydantic_settings import BaseSettingsModel, load_settings



class RunServerSettings(BaseSettings):
    port: int = 5555
    user: str = None

    class Config:
        env_prefix = 'MY_APP_RUNSERVER_'

class Settings(BaseSettings):
    debug: bool = True
    runserver: RunServerSettings = RunServerSettings()

    class Config:
        env_prefix = 'MY_APP_'

# c = ConfigManager(model=Settings, prefix='MY_APP')
settings = Settings(_env_file='test.env')

# @click.group(context_settings=dict(default_map=c.settings.dict() ))
@click.group(context_settings=dict(default_map=settings.dict() ))
# @click_config_option(c)
@click.option('--debug/--no-debug', help="Enable or disable debgging mode.", type=bool, show_default=True)
@click.pass_context
def cli(ctx, debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))
    click.echo(f'Context = {ctx.default_map}')
    click.echo(f'Climate: {settings.dict()}')



@cli.command()
# @click.option('--port', default=c.settings.runserver.port, show_default=True)
@click.option('--port', default=settings.runserver.port, show_default=True)
@click.option('--user', default="", prompt=True, show_default=True)
@click.pass_context
def runserver( ctx, port, user):
    click.echo(f'Serving {user} on http://127.0.0.1:{port}/' )
    click.echo(f'Context = {ctx.default_map}')
#    click.echo(f'Climate: {c.settings}')


def test_hello_world():
  runner = CliRunner()
  result = runner.invoke(cli, ['--debug', 'runserver'])
  print(result.stdout)
  assert result.exit_code == 0
  pytest.fail()

if __name__ == '__main__':
    cli()