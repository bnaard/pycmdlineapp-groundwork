from pycmdlineapp_groundwork.utility.typing import FilePathOrBuffer
import pytest
import tempfile
import requests
from pathlib import Path
from schema import Schema
from pycmdlineapp_groundwork.config.reader import ConfigurationReader, ConfigurationStreamReader
from pycmdlineapp_groundwork.config.config import ValidatedConfiguration


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
