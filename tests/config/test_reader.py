from pycmdlineapp_groundwork.utility.typing import FilePathOrBuffer
import pytest
import tempfile
import requests
from pathlib import Path
from schema import Schema, And, Use
from pycmdlineapp_groundwork.config.reader import ConfigurationReader, ConfigurationStreamReader, ConfigurationYAMLReader
from pycmdlineapp_groundwork.config.validated_configuration import ValidatedConfiguration


def test_configuration_reader():
    dummy_schema= Schema({}, ignore_extra_keys= True)
    cfg= ValidatedConfiguration(dummy_schema)
    reader= ConfigurationReader(cfg)
    assert hasattr(reader, "_configuration")
    assert reader._configuration == cfg


@pytest.fixture
def example_config_content():
    yield "foo: bar"


def test_configuration_stream_reader(example_config_content, httpserver):
    temp_dir= tempfile.TemporaryDirectory()
    temp_file_name= Path(temp_dir.name).joinpath(next(tempfile._get_candidate_names()))
    with open(temp_file_name, "w") as writer:
        writer.write(example_config_content)
    dummy_schema= Schema({}, ignore_extra_keys= True)
    cfg= ValidatedConfiguration(dummy_schema)

    stream_reader= ConfigurationStreamReader(filepath_or_buffer= str(temp_file_name), configuration= cfg)
    assert stream_reader._filepath_or_buffer == str(temp_file_name)
    stream_reader.load()
    assert stream_reader._read_configuration == example_config_content

    stream_reader= ConfigurationStreamReader(filepath_or_buffer= temp_file_name, configuration= cfg)
    assert stream_reader._filepath_or_buffer == temp_file_name
    stream_reader.load()
    assert stream_reader._read_configuration == example_config_content

    with open(temp_file_name, "r") as config_file:
        stream_reader= ConfigurationStreamReader(filepath_or_buffer= config_file, configuration= cfg)
        assert stream_reader._filepath_or_buffer == config_file
        stream_reader.load()
        assert stream_reader._read_configuration == example_config_content

    httpserver.expect_request("/foobar").respond_with_data(example_config_content, content_type="text/plain")
    assert requests.get(httpserver.url_for("/foobar")).text == example_config_content


def test_configuration_yaml_reader(example_config_content):
    temp_dir= tempfile.TemporaryDirectory()
    temp_file_name= Path(temp_dir.name).joinpath(next(tempfile._get_candidate_names()))
    with open(temp_file_name, "w") as writer:
        writer.write(example_config_content)
    dummy_schema= Schema({str: And(str, Use(str.upper))}, ignore_extra_keys= True)
    cfg= ValidatedConfiguration(dummy_schema)
    stream_reader= ConfigurationYAMLReader(filepath_or_buffer= temp_file_name, configuration= cfg)
    stream_reader.load()
    stream_reader.parse()
    assert stream_reader._parsed_configuration == {"foo": "bar"}
    stream_reader.merge()
    assert "foo" in cfg._configuration
    assert cfg._configuration["foo"] == "bar"
    stream_reader.validate()
    assert "foo" in cfg._configuration
    assert cfg._configuration["foo"] == "BAR"
