# use the zoomcamp image that contains the following:
#FROM python:3.13.5-slim-bookworm
#WORKDIR /code
#COPY pipeline_v2.bin .


FROM --platform=linux/amd64 agrigorev/zoomcamp-model:2025

# Install uv for dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# set the working dir to code
WORKDIR /code

# Add the virtual environment's bin directory to the PATH so Python tools work globally
ENV PATH="/code/.venv/bin:$PATH"

# copy the following files to install the dependendcies in the container
COPY "pyproject.toml" "uv.lock" ".python-version" ./

# install the dependencies
RUN uv sync  --locked

# copy the fastAPI web service predict file
COPY "predict.py" ./

# open the port 9696 to it can be accessed from outside the container
EXPOSE 9696

# create an entrypoint to the container
ENTRYPOINT ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "9696"]



