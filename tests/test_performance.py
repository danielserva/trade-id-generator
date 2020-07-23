# -*- coding: utf-8 -*-

import re
import mock
import pytest
from concurrent.futures import ThreadPoolExecutor
from identity.generation import generate, generate_bulk

ID_CHARACTERS = '0ABCDEFG'
MAX_ID_COUNT = 7 ** len(ID_CHARACTERS) - 1


@pytest.mark.timeout(180)
def test_generate_bulk_performance():
    """This needs to run in a clean enironment, so if you are using any
    external persistence, clear it before running this."""
    with mock.patch('identity.generation.ID_CHARACTERS', ID_CHARACTERS):
        ids = list(generate_bulk(5000000))
    assert True
