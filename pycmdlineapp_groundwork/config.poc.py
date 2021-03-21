import click
from click.testing import CliRunner
import pytest

import yaml
import json
from pathlib import Path
from typing import Dict, Any

from pydantic import BaseSettings, BaseModel

config_file_user_home= "~/config.yaml"
config_file_cwd= "./config.yaml"


def json_config_settings_source(settings: BaseSettings) -> Dict[str, Any]:
    """
    A simple settings source that loads variables from a YAML file
    """
    encoding = settings.__config__.env_file_encoding
    config_file= Path(config_file_cwd)
    if not config_file.is_file(): 
        config_file= Path(config_file_user_home)
        if not config_file.is_file():
            return {}

    try:
        with open(config_file, 'r') as stream:
            return yaml.safe_load(stream)
    except yaml.YAMLError as e:
        raise Exception(
            f"Error parsing config file from {config_file}. {e}") from e
    except Exception as e:
        raise Exception(
            f"Error loading config file from {config_file}. {e}") from e
    return {}



class BaseSettingsConfig:

    @classmethod
    def customise_sources(
        cls,
        init_settings,
        env_settings,
        file_secret_settings,
    ):
        return (
            init_settings,
            env_settings,
            json_config_settings_source,
            file_secret_settings,
        )


class RunServerSettings(BaseModel):
    port: int = 5000

class DefaultMap(BaseModel):
    debug: bool = False
    runserver: RunServerSettings = RunServerSettings()

class Settings(BaseSettings):
    default_map: DefaultMap = DefaultMap()

    class Config(BaseSettingsConfig):
        env_prefix = 'MY_APP_' 
        config_file_user_home= "~/myapp.yaml"
        config_file_cwd= "./myapp.yaml"


# Order of precendence for default values, input to command line options, 
# lowest to highest, higher overwrites lower
# 1. default values
# 2. .env files
# 3. environment variables set outside .env file
# 4. default config file config.yaml in current working directory
# 5. default config file config.yaml in user home
# then command-line parsing
settings= Settings(_env_file='.env')
CONTEXT_SETTINGS= settings.dict()
# CONTEXT_SETTINGS = dict(
#     default_map={'runserver': {'port': 5000}}
# )


def config_option(
    settings: BaseSettings,
    *param_decls,
    **kwargs,
):
    """Add a ``--config`` option which loads a config file and replaces the set content
    in the application's global settings.
    """
    if settings is None:
        raise click.BadParameter(
            f"No settings object available to store configuration."
        )
    else:
        pass


    def callback(ctx, param, value):
        if not value or ctx.resilient_parsing:
            return
        try:
            path_to_config= Path(value)
        except:
            raise click.BadParameter(f'"{value}" is not a valid path to config file in --{param}-option.')

        if not path_to_config.is_file():
            raise click.BadParameter(f'In --{param}-option: "{value}" file not found or not a valid file. {text: {"Maybe it is a directory?" if path_to_config.is_dir() else "" }}')

    if not param_decls:
        param_decls = ("--config",)

    kwargs.setdefault("expose_value", False)
    kwargs.setdefault("is_eager", True)
    kwargs.setdefault("help", "Load configuration from specified file.")
    kwargs.setdefault("type", str)
    kwargs["callback"] = callback
    return click.option(*param_decls, **kwargs)





@click.group(context_settings=CONTEXT_SETTINGS)
# @click.group()
@click.option('--debug/--no-debug')
def cli(config, debug):
    click.echo('Debug mode is %s' % ('on' if debug else 'off'))


@cli.command()
@config_option(settings)
@click.option('--port', default=8000)
@click.option('--user', default="", prompt=True)
def runserver(port, user):
    click.echo('Serving on http://127.0.0.1:%d/' % port)

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