import os
import configparser
import pytest
import platform
import distro
import google.generativeai as genai

from infra.config import get_config, set_key, set_model, ask_ai

# Fixtures
@pytest.fixture
def config_file(tmp_path):
    config_path = tmp_path / "test_config.ini"
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'api_key': 'test_api_key', 'model': 'test_model'}
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    return config_path

# Tests
def test_get_config(config_file, monkeypatch):
    monkeypatch.setenv('HOME', str(config_file.parent))
    api_key, model = get_config()
    assert api_key == 'new_api_key'
    assert model == 'new_model'

def test_set_key(config_file, monkeypatch):
    monkeypatch.setenv('HOME', str(config_file.parent))
    set_key('new_api_key')
    config = configparser.ConfigParser()
    config.read(config_file)
    assert config.get('DEFAULT', 'api_key') == 'test_api_key'

def test_set_model(config_file, monkeypatch):
    monkeypatch.setenv('HOME', str(config_file.parent))
    set_model('new_model')
    config = configparser.ConfigParser()
    config.read(config_file)
    assert config.get('DEFAULT', 'model') == 'test_model'

# Mock the GenerativeModel class
@pytest.fixture
def mock_generative_model(monkeypatch):
    class MockGenerativeModel:
        def __init__(self, model_name):
            self.model_name = model_name

        def generate_content(self, prompt):
            return genai.GenerativeResponse(candidates=[genai.GenerativeResponseCandidate(content=genai.GenerativeContent(parts=[genai.GenerativeContentPart(text="Mock response")]))])

    monkeypatch.setattr(genai, 'GenerativeModel', MockGenerativeModel)

def test_ask_ai_with_mock(mock_generative_model, capsys):
    api_key = 'test_api_key'
    prompt = 'Test prompt'
    response = ask_ai(prompt, api_key)
    captured = capsys.readouterr()
    assert "" in captured.out
