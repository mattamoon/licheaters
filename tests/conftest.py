import pytest
from src.gathercheater.functions import configure
from src.gathercheater.gathercheater import GatherCheater


@pytest.fixture(scope='session')
def api_access():
    configure()
    lichess = GatherCheater()
    return lichess
