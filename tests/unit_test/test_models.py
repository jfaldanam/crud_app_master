import pytest

from crud_api.models import Project
from pydantic import ValidationError

def test_time_cant_be_negative():
    with pytest.raises(ValidationError):
        Project(name="test", time=-1)

