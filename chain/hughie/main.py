import logging.config
from importlib import import_module

from chain.common.log import DEFAULT_LOGGING

# We're using gevent because our tasks are IO intensive. For that we need to monkeypatch
# everyhing. More info: https://huey.readthedocs.io/en/latest/troubleshooting.html
from gevent import monkey

monkey.patch_all()

# Setup logging
logging.config.dictConfig(DEFAULT_LOGGING)

# This import is needed for a correct start of huey workers
from .config import huey  # noqa

# TODO: put this somewhere in config so it's extensible, or even as part of a plugin
# setup
TASK_MODULES = ["chain.plugins.peers.tasks"]

for task_module in TASK_MODULES:
    import_module(task_module)
