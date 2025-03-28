import sqlite3

def check_if_project_exists(project_name: str) -> bool:
    """Check in the database if the project exists.

    This function expects a SQLite database in the current folder.

    To search if a project exists, it filters name.

    :raises ValueError: Database not found. Check the database is in the current folder.

    :param project_name: The name of a project in the database, will be used for search.

    :return: Returns whether the project exists or not
    """
    with sqlite3.connect("project_database.db") as connection:
        cursor = connection.cursor()

        results = cursor.execute("SELECT name from Project p where p.name = ?", (project_name,)).fetchone()
        print(f"Executing ->SELECT name from Project p where p.name = '{project_name}'")

        if results is None:
            return False
        else:
            return True
        

def get_all_projects():
    with sqlite3.connect("project_database.db") as connection:
        cursor = connection.cursor()
        results = cursor.execute("Select * from Project ").fetchall()

        projects = []
        for name, time in results:
            projects.append({"name": name, "time": time})
    
    return projects
