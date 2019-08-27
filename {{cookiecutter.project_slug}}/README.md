# {{ cookiecutter.project_name }}
[![Python Version: {{ cookiecutter.python_version }}](https://badgen.net/badge/python/{{ cookiecutter.python_version }}/green)](https://docs.python.org/{{ cookiecutter.python_version }}/)
{%- if cookiecutter.use_black|lower == 'y' -%} [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/python/black)

## Black
이 프로젝트는 Black을 사용합니다. [Black#editor_integration](https://black.readthedocs.io/en/stable/editor_integration.html) 문서를 참조해 사용 중인 에디터에 Black을 연동하세요.
{%- endif %}
