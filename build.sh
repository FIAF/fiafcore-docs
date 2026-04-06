# build fiafcore-docs-dev image.

docker build -t fiafcore-docs-dev .

# build fiafcore-docs-example image.

# docker build -t fiafcore-docs-example example

# deploy fiafcore-docs containers.

docker compose up -d
