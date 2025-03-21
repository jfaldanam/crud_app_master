FROM python

# Set the workdir where we will run all commands
WORKDIR /code/crud_api/

# Copy the code and project files to a standard location
COPY src pyproject.toml README.md /code/crud_api/

# Install the crud_api module
RUN python -m pip install .

# Run the API
ENTRYPOINT [ "python", "-m", "crud_api", "--port", "8000" ]