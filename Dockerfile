# Run from the root of a project that contains your model files:
#   docker build -t ddlml .
#   docker run --rm \
#     --user "$(id -u):$(id -g)" -v "$PWD:/work" \
#     ddlml \
#     examples/simple_example/database.yaml \
#     --docs docs \
#     --output output.yaml
#
# This writes the documentation to docs/database/ and the validated model to
# output.yaml, both relative to the mounted folder.

FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.13.8 /uv /bin/uv
WORKDIR /app
COPY . .
RUN uv sync --frozen --no-dev
ENV PATH="/app/.venv/bin:$PATH"
WORKDIR /work
ENTRYPOINT ["ddlml"]
CMD ["--help"]
