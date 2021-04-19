import click
from pydantic import BaseSettings, ValidationError
from typing import Sequence, TypeVar, Dict, cast
from pathlib import Path

from ..utility.dict_deep_update import dict_deep_update
from .config_file_loaders import DictLoadError, load_dict_from_file


SettingsClassType = TypeVar("SettingsClassType", bound=BaseSettings)


def click_config_option(
    settings_obj: BaseSettings,
    settings_class_type: SettingsClassType,
    click_obj=click,
    option_name: str = "config",
    option_short: str = "",
    **kw,
):
    def validate(ctx: click.Context, param, value):
        if not value:
            return list()
        if not isinstance(value, Sequence):
            value = [value]
        config_map = {}
        for config_file in value:
            config_file = Path(config_file).resolve()
            try:
                config_map[str(config_file)] = load_dict_from_file(config_file)
            except DictLoadError as e:
                click.echo(
                    f"{e.message}\nContext:\n{e.document}\nPosition = {e.position},"
                    f" line number = {e.line_number}, column_number = {e.column_number}"
                )
                ctx.abort()

        target_config_dict = settings_obj.dict()
        new_settings_obj: BaseSettings = None
        for config_file, config_dict in config_map.items():
            try:
                dict_deep_update(
                    target_config_dict, cast(Dict[object, object], config_dict)
                )
            except RecursionError as e:
                click.echo(
                    f"Error reading {config_file}.\nData structure depth exceeded.\n{e}"
                )
                ctx.abort()
            except ValueError as e:
                click.echo(f"{e}")
                ctx.abort()

            try:
                new_settings_obj = settings_class_type.parse_obj(target_config_dict)
            except ValidationError as e:
                click.echo(f"Validation error for config file {config_file}.\n{e}")
                ctx.abort()

        ctx.default_map = new_settings_obj.dict()
        return new_settings_obj

    option_kwargs = dict(
        help="Config file path for loading settings from file.",
        callback=validate,
        type=click.Path(exists=True, dir_okay=False, resolve_path=True),
        expose_value=True,
        is_eager=True,
        multiple=True,
    )
    option_kwargs.update(kw)
    option_short = (
        option_short.lstrip("-")
        if option_short.lstrip("-") != ""
        else f"-{option_name[0]}"
    )
    option_name = option_name.lstrip("-")
    option = click_obj.option(f"--{option_name}", f"-{option_short}", **option_kwargs)
    return option
