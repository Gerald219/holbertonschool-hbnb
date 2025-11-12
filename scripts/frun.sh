#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
lsof -ti :5001 | xargs -r kill -9
export FLASK_APP=part3.app:create_app
export FLASK_DEBUG=1
flask run -p 5001
