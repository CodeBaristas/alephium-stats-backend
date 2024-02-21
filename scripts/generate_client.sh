#!/usr/bin/env sh

# PROJECT_NAME="alephium-stats-backend"
PROJECT_NAME=$(basename $PWD)
MODULE_NAME=$(echo "$PROJECT_NAME" | cut -d'-' -f1-2 | tr '-' '_')

CLIENT_PATH="../$PROJECT_NAME-client"

export APP_NAME=$PROJECT_NAME
export APP_CONFIG=dev

# dump openapi.json
python3 -c "
import json

from fastapi.openapi.utils import get_openapi

from $MODULE_NAME.app import app

with open('data/openapi.json', 'w') as f:
    json.dump(get_openapi(
        title=app.title,
        version=app.version,
        openapi_version=app.openapi_version,
        description=app.description,
        routes=app.routes,
    ), f)
  " &&
	./node_modules/.bin/openapi-generator-cli generate \
		-i 'data/openapi.json' \
		-o $CLIENT_PATH/client \
		-g typescript-axios &&
	cd $CLIENT_PATH &&
	npm run build &&
	git add . &&
	git commit -am "AUTO" &&
	git push
