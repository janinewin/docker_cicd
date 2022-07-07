# Start from Python 3.8.10, the slim version is usually enough (stripped from packages that aren't useful for our purpose)
# and way smaller than the non-slim version
FROM python:3.8.10-slim

# Setting PYTHONUNBUFFERED to 1 is useful for logs
# See https://stackoverflow.com/a/59812588
ENV PYTHONUNBUFFERED 1

# Set a working directory that maps our data-engineering-challenges repository structure
# so that relative imports like ../../../common/lewagonde work within the Docker image
WORKDIR /repo/02-Advanced-data-pipelines/02-Data-transformation/02-Image-Transformation/

# Install Poetry
RUN pip3 install --upgrade --no-cache-dir pip \
    && pip3 install poetry

# Copy the installation files and local dependencies first
COPY poetry.lock pyproject.toml ./
COPY build/common/lewagonde/ /repo/common/lewagonde/

# Now we are ready to install the packages
RUN poetry install --no-dev

# Copy this package's Python files last
COPY ./ ./

# Run the `streamlit run` command on port 8080
CMD ["poetry", "run", "streamlit", "run", "lwface/face.py", "--server.port", "8080"]

# --> Delete this line when you've read the full Dockerfile, so the `test_dockerfile` test passes ;)
