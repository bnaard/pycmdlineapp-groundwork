# Contributing

We'd be happy to get your contribution to this project!

## Issues

Questions, feature requests and bug reports are all welcome as [discussions or issues](https://github.com/bnaard/pycmdlineapp-groundwork/issues).

## Security Policy

tbd

## Pull Requests

It's simple to get started and create a Pull Request. *pycmdlineapp_groundwork* has few dependencies, doesn't require compiling and tests don't need access to databases, etc.

*pycmdlineapp_groundwork* is released regularly so you should see your improvements release in a matter of weeks.

!!! note
    Unless your change is trivial (typo, docs tweak etc.), please create an issue to discuss the change before
    creating a pull request.

If you're looking for immediate possibilities to contribute, look out for the label ["help wanted"](https://github.com/github.com/bnaard/pycmdlineapp-groundwork/issues?q=is%3Aopen+is%3Aissue+label%3A%22help+wanted%22) in [issues]((https://github.com/bnaard/pycmdlineapp-groundwork/issues)).

### Prerequsites

- Mandatory: You need [python-poetry](https://python-poetry.org/) installed.
- Optionally: You can work with [VS Code](https://code.visualstudio.com/) and [development containers](https://github.com/microsoft/vscode-dev-containers). See [Optional VS Code Setup description](#optional-vs-code-setup).

### Development setup

Please follow these steps to contribute:

1. Clone your fork and cd into the repo directory

```bash
git clone git clone https://github.com/bnaard/pycmdlineapp-groundwork.git
cd pycmdlineapp-groundwork
```

2. Set up a virtualenv and install dependencies

```bash

```

https://github.com/bnaard/pycmdlineapp-groundwork.git

To make contributing as easy and fast as possible, you'll want to run tests and linting locally. Luckily,
*pydantic* has few dependencies, doesn't require compiling and tests don't need access to databases, etc.
Because of this, setting up and running the tests should be very simple.

You'll need to have **python 3.6**, **3.7**, **3.8**, or **3.9**, **virtualenv**, **git**, and **make** installed.

```bash
# 1. clone your fork and cd into the repo directory
git clone git@github.com:<your username>/pydantic.git
cd pydantic

# 2. Set up a virtualenv for running tests
virtualenv -p `which python3.7` env
source env/bin/activate
# (or however you prefer to setup a python environment, 3.6 will work too)

# 3. Install pydantic, dependencies, test dependencies and doc dependencies
make install

# 4. Checkout a new branch and make your changes
git checkout -b my-new-feature-branch
# make your changes...

# 5. Fix formatting and imports
make format
# Pydantic uses black to enforce formatting and isort to fix imports
# (https://github.com/ambv/black, https://github.com/timothycrosley/isort)

# 6. Run tests and linting
make
# there are a few sub-commands in Makefile like `test`, `testcov` and `lint`
# which you might want to use, but generally just `make` should be all you need

# 7. Build documentation
make docs
# if you have changed the documentation make sure it builds successfully
# you can also use `make docs-serve` to serve the documentation at localhost:8000

# ... commit, push, and create your pull request
```

## Optional VS Code setup

tbd
