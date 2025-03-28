import pytest

from crud_api.models import Project
from pydantic import ValidationError

def test_time_cant_be_negative():

    project = Project(name="test", time=-1)

    assert project.time == 0, "A negative time should be defaulted to zero"

