# build fiafcore-docs-dev image.

docker build -t fiafcore-docs-dev .

# build fiafcore-docs-example image.

docker build -t fiafcore-docs-example .

# deploy containers.

docker compose up -d
