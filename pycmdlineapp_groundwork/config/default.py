

CONFIG_FILE_LOCAL_DEFAULT= "./app.ini"
CONFIG_FILE_USERHOME_DEFAULT = "~/.app/app.ini"
CONFIG_DEFAULT_YAML= ''' 

# General Configuration Options

general:

    # verbosity level for more output during program execution. Affects the handlers, not the loggers.
    # Not set (default) for no change compared to base settings for each logger in this file
    # -v => +1 level for each logger (eg. CRITICAL => ERROR)
    # -vv => +2 levels for each logger (eg. CRITICAL => WARNING) 
    # -vvv => +3 levels for each logger (eg. CRITICAL => INFO) 
    # -vvvv => +4 levels for each logger (eg. CRITICAL => DEBUG) 
    verbose: 0
    


# Python Logging configuration

# see https://docs.python.org/3/howto/logging.html and https://docs.python.org/3/library/logging.config.html for options
# schema: https://docs.python.org/3/library/logging.config.html#configuration-dictionary-schema 

logging:
    version: 1
    disable_existing_loggers: False
    root:
        level: DEBUG
        handlers: ["rotatingFileHandler"]
    loggers:
        app:
            level: DEBUG
            handlers: ["consoleHandler", "rotatingFileHandler"]
            propagate: False
            qualname: app
        app.echo:
            level: INFO
            handlers: ["echoHandler"]
            propagate: False
            qualname: app.echo
    handlers:
        consoleHandler:
            class : logging.StreamHandler
            formatter: consoleColoredFormatter
            level : CRITICAL
            stream : ext://sys.stdout
        rotatingFileHandler:
            class : logging.handlers.RotatingFileHandler
            formatter: fileFormatter
            level: INFO
            filename: app.log
            maxBytes: 500000
            backupCount: 5
        echoHandler:
            class: logging.StreamHandler
            formatter: echoColoredFormatter
            level: CRITICAL
            stream: ext://sys.stdout
    formatters:
        consoleColoredFormatter:
            class: coloredlogs.ColoredFormatter
            style: "{"
            format: "{levelname:<10}{name}: {message}"
            datefmt: ""
        fileFormatter:
            class: logging.Formatter
            style: "{"
            format: "%(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [-] %(message)s"
            datefmt: ""
        echoColoredFormatter:
            class: coloredlogs.ColoredFormatter
            style: "{"
            format: "{message}"
            datefmt: ""
'''

