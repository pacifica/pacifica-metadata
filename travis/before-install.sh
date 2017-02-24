#!/bin/bash -xe
sudo rm -f /usr/local/bin/docker-compose
sudo curl -L -o /usr/local/bin/docker-compose https://github.com/docker/compose/releases/download/${DOCKER_COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)
sudo chmod +x /usr/local/bin/docker-compose

case "$TRAVIS_PYTHON_VERSION" in
  pypy) export PYPY_VERSION="pypy-2.6.1" ;;
  pypy3) export PYPY_VERSION="pypy3-2.4.0" ;;
esac
if ! [ -z "$PYPY_VERSION" ] ; then
  export PYENV_ROOT="$HOME/.pyenv"
  if [ -f "$PYENV_ROOT/bin/pyenv" ]; then
    pushd "$PYENV_ROOT" && git pull && popd
  else
    rm -rf "$PYENV_ROOT" && git clone --depth 1 https://github.com/yyuu/pyenv.git "$PYENV_ROOT"
  fi
  "$PYENV_ROOT/bin/pyenv" install "$PYPY_VERSION"
  virtualenv --python="$PYENV_ROOT/versions/$PYPY_VERSION/bin/python" "$HOME/virtualenvs/$PYPY_VERSION"
  source "$HOME/virtualenvs/$PYPY_VERSION/bin/activate"
fi
if [ "$RUN_LINTS" = "true" ]; then
  pip install pre-commit
else
  pip install codeclimate-test-reporter coverage nose pytest
fi
sudo service postgresql stop
