import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Response

from crud_api.utils import check_if_project_exists, get_all_projects
from crud_api.models import Project

@asynccontextmanager
async def sqlite_lifespan(app: FastAPI):
    global DB_CONNECTION
    # Load the ML model
    with sqlite3.connect("project_database.db") as connection:
        print("[DB] Starting connection")
        DB_CONNECTION = connection
        cursor = connection.cursor()

        cursor.execute("""
CREATE TABLE IF NOT EXISTS Project (
    name TEXT PRIMARY KEY,
    time INTEGER
)
""") 
        connection.commit()
        yield
        # Clean DB connection
    print("[DB] Closing connection")


DB_CONNECTION = None

app = FastAPI(
    lifespan=sqlite_lifespan
)


@app.post("/api/v1/project/{project_name}")
def create_project(project_name: str):
    "Create a project, if it already exists returns a 4XX error"
    if check_if_project_exists(project_name):
        raise HTTPException(status_code=418,detail="The project already exists")
    
    with sqlite3.connect("project_database.db") as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO Project (name, time) VALUES ( ?, ?)", (project_name, 0))
        print("Project created succesfully")
        connection.commit()


@app.get("/api/v1/project")
def list_all_projects() -> list[Project]:
    return get_all_projects()


# TODO: Log time
@app.post("/api/v1/project/{project_name}/log")
def log_time(project_name: str, time_to_log: int):

    if not check_if_project_exists(project_name):
        raise HTTPException(status_code=404, detail="Project not found")
    # Ideally, all this should be done on a single transaction
    with sqlite3.connect("project_database.db") as connection:
        cursor = connection.cursor()

        result = cursor.execute("SELECT name, time from Project p where p.name = ?", (project_name,)).fetchone()

        project = Project(name=result[0], time=result[1])

        project.time += time_to_log

        cursor.execute("UPDATE Project set time = ?  where name = ?", (project.time, project.name))

        connection.commit()

    return {"message": "Time updated succesfully"}
        


# TODO: delete project
@app.delete("/api/v1/project/{project_name}")
def delete_project(project_name: str):
    if not check_if_project_exists(project_name):
        raise HTTPException(status_code=404, detail="Project not found")

    with sqlite3.connect("project_database.db") as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM Project WHERE name = ?", (project_name,))
        connection.commit()
        return {"message": "Project deleted successfully"}

# TODO: snapshot

@app.get("/api/v1/project/{project_name}/snapshot")
def create_snapshot(project_name: str) -> str:
    projects = get_all_projects()

    file_content = "NAME,TIME\n"

    for project in projects:
        file_content += f"{project['name']},{project['time']}\n"
    
    return Response(content=file_content, media_type='text/csv')