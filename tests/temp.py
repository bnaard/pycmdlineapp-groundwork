import click
from click.testing import CliRunner
from pydantic import BaseSettings
from pycmdlineapp_groundwork import click_config_option
from tempfile import mkdtemp
from shutil import rmtree
from pathlib import Path

# create a temporary config file
dirpath = mkdtemp()
temp_config_name = Path(dirpath) / "config.ini"
temp_config = open(temp_config_name, "wt")
_ = temp_config.writelines(['debug = False\n', 'port = 4242'])
temp_config.close()
class Settings(BaseSettings):
     debug: bool = False
     port: int = 1234
settings = Settings()
@click.command(context_settings=dict(default_map=settings.dict() ))
@click_config_option(settings, Settings)
@click.option('--debug/--no-debug', default=settings.debug, help="debug", type=bool, show_default=True)
@click.pass_context
def cli(ctx, config, debug):
    click.echo(f'Config is {config}')
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))
    click.echo(f'Context = {ctx.default_map}')

# Simulate calling the commandline app to show usage of config-option
print(temp_config_name.read_text())
runner = CliRunner()
result = runner.invoke(cli, ['--debug', '--config', str(temp_config_name) ])
print(result.stdout)


# if __name__ == '__main__':
#     cli()
rmtree(dirpath)
