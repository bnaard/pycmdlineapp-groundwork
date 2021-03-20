
import click
from pydantic import BaseModel, BaseSettings
from pydantic_settings import BaseSettingsModel, load_settings


def click_config_option(
    settings_obj: BaseModel, click_obj=click, option_name="config", **kw
):

    def validate(ctx, param, value):
        if value:
            load_settings()
            settings_obj.settings_files = value
            settings_obj.reload()
            ctx.default_map= settings_obj.settings.dict()

    option_kwargs = dict(
        help="Config file path for loading settings from file.",
        callback=validate,
        type=click.Path(exists=True, dir_okay=False, resolve_path=True),
        expose_value=False,
        is_eager=True,
        multiple=True,
    )
    option_kwargs.update(kw)
    option = click_obj.option(
        "--{}".format(option_name), "-{}".format(option_name[0]), **option_kwargs
    )
    return option
