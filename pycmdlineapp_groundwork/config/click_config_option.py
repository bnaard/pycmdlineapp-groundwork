

import click
import yaml
import toml
import json
from pydantic import BaseSettings
from typing import Sequence, TypeVar
from pathlib import Path

from ..utility.dict_deep_update import deepupdate



SettingsClassType = TypeVar("SettingsClassType")




def click_config_option(
    settings_obj: BaseSettings,
    settings_class_type: SettingsClassType,
    click_obj=click,
    option_name="config",
    **kw
):
    def validate(ctx, param, value):
        if not value:
            return list()
        if isinstance(value, Sequence):
            value = value
        config_map = {}
        for config_file in value:
            config_file = Path(config_file).resolve()
            if config_file.suffix.lower() in [".json", ".jsn"]:
                config_map[str(config_file)] = json.loads(config_file.read_text())
            elif config_file.suffix.lower() in [
                ".toml",
                ".tml",
                ".ini",
                ".config",
                ".cfg",
            ]:
                config_map[str(config_file)] = toml.load(config_file)
            elif config_file.suffix.lower() in [".yml", ".yaml"]:
                config_map[str(config_file)] = yaml.safe_load(config_file.read_text())
        target_config_dict = settings_obj.dict()
        for _, config_dict in config_map.items():
            deepupdate(target_config_dict, config_dict)
        new_settings_obj = settings_class_type.parse_obj(target_config_dict)
        ctx.default_map = new_settings_obj.dict()

        # return target_config_dict
        # return new_settings_obj.dict()
        return config_map
        # settings_obj.settings_files = value
        # settings_obj.reload()
        # ctx.default_map= settings_obj.settings.dict()

    option_kwargs = dict(
        help="Config file path for loading settings from file.",
        callback=validate,
        type=click.Path(exists=True, dir_okay=False, resolve_path=True),
        expose_value=True,
        is_eager=True,
        multiple=True,
    )
    option_kwargs.update(kw)
    option = click_obj.option(
        "--{}".format(option_name), "-{}".format(option_name[0]), **option_kwargs
    )
    return option