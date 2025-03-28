import sqlite3
from tempfile import TemporaryDirectory
from pathlib import Path

def setup():
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

        cursor.execute("""
CREATE TABLE IF NOT EXISTS Project (
    name TEXT PRIMARY KEY,
    time INTEGER
)
""")    
        cursor.execute("INSERT INTO Project (name, time) VALUES ( ?, ?)", ("project1", 0))
        cursor.execute("INSERT INTO Project (name, time) VALUES ( ?, ?)", ("project2", 95))
        connection.commit()



def test_check_if_project_exists():
    pass

setup()