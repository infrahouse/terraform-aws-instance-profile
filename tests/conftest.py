import logging

import pytest
from infrahouse_core.logging import setup_logging

LOG = logging.getLogger()
TERRAFORM_ROOT_DIR = "test_data"


setup_logging(LOG, debug=True)


def pytest_addoption(parser):
    parser.addoption(
        "--run-cis-e2e",
        action="store_true",
        default=False,
        help="Run the slow ad-hoc Amazon Inspector CIS end-to-end scan test.",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers",
        "cis_e2e: slow ad-hoc end-to-end test running a real Amazon Inspector CIS scan",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-cis-e2e"):
        return
    skip_cis = pytest.mark.skip(reason="needs --run-cis-e2e option to run")
    for item in items:
        if "cis_e2e" in item.keywords:
            item.add_marker(skip_cis)
