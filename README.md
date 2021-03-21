<!-- markdownlint-disable MD025 MD041 -->

[![Build](https://github.com/bnaard/pycmdlineapp-groundwork/workflows/Build/badge.svg?event=push)](https://github.com/bnaard/pycmdlineapp-groundwork/actions?query=event%3Apush+branch%3Amaster+workflow%3ABuild)
[![Docs](https://github.com/bnaard/pycmdlineapp-groundwork/workflows/Docs/badge.svg?event=push)](https://github.com/bnaard/pycmdlineapp-groundwork/actions?query=event%3Apush+branch%3Amaster+workflow%3ADocs)
[![license](https://img.shields.io/github/license/bnaard/pycmdlineapp-groundwork.svg)](https://github.com/bnaard/pycmdlineapp-groundwork/blob/master/LICENSE.md)
[![Coverage](https://codecov.io/gh/bnaard/pycmdlineapp-groundwork/branch/master/graph/badge.svg)](https://codecov.io/gh/bnaard/pycmdlineapp-groundwork)

# Welcome to pycmdlineapp_groundworks

pycmdlineapp_groundworks is an opinionated collection of libraries, code and best-practice descriptions to jumpstart the development for mid-level to complex python command-line applications.

## Features

The toolset solves the following challenges:

| Challenge           | I would like to have ...             | Solution       |
| :------------------ | :----------------------------------- | :------------- |
| Commandline parsing | Mulit-/Subcommand with arguments and options (all forms, like single, multiple, typed, with prompt, ...), validated and with automatic help | [click](https://click.palletsprojects.com/en/7.x/) provides all, is stables has an excellent help and a large community |
| Settings management | Schema-validated, documented and probably pre-processed settings from different sources (config files, environment variables, .env files, secret files), coordinated with click default values and input from command-line arguments  | Using [pydantic](https://pydantic-docs.helpmanual.io/) in connection with [climatecontrol](https://github.com/daviskirk/climatecontrol/tree/master/climatecontrol) for missing features (multi-config-file load & merge, config-file format support for toml/yaml/json, environment variables for nested configs like for click-subcommands) and docstring extraction from [pydantic-settings](https://github.com/danields761/pydantic-settings) |
| Logging setup       | Flexible, configurable, thread-safe logging setup writing to multiple destinations (console, files, network targets, ...) and with verbosity configurable from commandline | [Python standard logging](https://docs.python.org/3/howto/logging.html) facilities in combination with commandline parsing and settings management |
| Multi-progress bar  | Thread-safe colored progressbar with options for multiple bars, counters and clutter-free printing of log-/error-messages | Using [enlighten](https://github.com/Rockhopper-Technologies/enlighten) progress-bar library |
| Factory methods     | Ability to create objects with a factory-class based on enum types (example use case: message objects created by a message-provider-class) | Factory implementation inspired by [https://realpython.com/factory-method-python/](https://realpython.com/factory-method-python/) |

## Install

tbd

## Quick Start

tbd

For further details please see [usage documentation]()

## Documentation

[Documentation](https://bnaard.github.io/pycmdlineapp-groundwork/index.html)
