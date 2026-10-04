#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
# A busy port should report an error, never terminate another application.
exec flask --app part3.app:create_app run --debug --port "${PORT:-5001}"
