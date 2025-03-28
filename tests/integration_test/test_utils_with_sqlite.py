import sqlite3
from tempfile import TemporaryDirectory
from pathlib import Path
import pytest

from crud_api.utils import check_if_project_exists
from crud_api.models import Project

@pytest.fixture
def setup_data():
    return [("project1", 0), ("project2",95)]

@pytest.fixture
def db_setup(setup_data):
    """ This test requires:
    - There is a database we can connect to
    - The database has the required tables created
    - There is data in the tables
    """
    #directory = TemporaryDirectory()
    folder = Path("./test_data")
    folder.mkdir(exist_ok=True)
    with sqlite3.connect(folder/"project_database.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DROP TABLE Project")
        cursor.execute("""
CREATE TABLE IF NOT EXISTS Project (
    name TEXT PRIMARY KEY,
    time INTEGER
)
""")    
        
        for data in setup_data:
            cursor.execute("INSERT INTO Project (name, time) VALUES ( ?, ?)", data)
        
        print(cursor.execute("select * from Project").fetchall())
        connection.commit()

        return connection

def test_table_schema_includes_name_and_time(db_setup: sqlite3.Connection):
    """ Check if the table schema includes 'name' and 'time' columns """
    cursor = db_setup.cursor()
    cursor.execute("PRAGMA table_info(Project)")
    columns = [column[1] for column in cursor.fetchall()]  # Extract column names
    assert "name" in columns, "'name' column MUST exist in the schema"
    assert "time" in columns, "'time' column MUST exist in the schema"

def test_check_if_project_exists(db_setup: sqlite3.Connection, setup_data: list[tuple]):
    """ Check if the project exists in the database
     
    This test requires:
    - There is a database we can connect to
    - The database has the required tables created
    - There is data in the tables
    """
    for element in setup_data:
        does_exist = check_if_project_exists(element[0])
        assert does_exist, "This project MUST exist"

def test_check_if_project_does_not_exist(db_setup: sqlite3.Connection):
    does_exist = check_if_project_exists("project3")
    assert not does_exist, "This project MUST NOT exist"

def test_database_matches_pydantic_model(db_setup: sqlite3.Connection):
    """ Check if the data in the database matches the Pydantic model """
    cursor = db_setup.cursor()
    cursor.execute("SELECT * FROM Project")
    rows = cursor.fetchall()

    for row in rows:
        # Convert database row to dictionary
        project_data = {"name": row[0], "time": row[1]}
        # Validate with Pydantic model
        project = Project(**project_data)
        assert project.name == project_data["name"], "Project name MUST match"
        assert project.time == project_data["time"], "Project time MUST match"