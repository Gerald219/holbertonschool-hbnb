#!/usr/bin/env bash
set -euo pipefail
set +H  # avoid '!' expansion breaking JSON

BASE_URL="${BASE_URL:-http://127.0.0.1:5001/api/v1}"

# -- users and tokens --
EMAIL="guest@test"; PASS="pw"
curl -s -X POST "$BASE_URL/users/" -H "Content-Type: application/json" \
  -d "{\"first_name\":\"Guest\",\"last_name\":\"User\",\"email\":\"$EMAIL\",\"password\":\"$PASS\"}" >/dev/null
GUEST_TOKEN=$(curl -s -X POST "$BASE_URL/auth/login" -H "Content-Type: application/json" \
  -d "{\"email\":\"$EMAIL\",\"password\":\"$PASS\"}" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')

curl -s -X POST "$BASE_URL/users/" -H "Content-Type: application/json" \
  -d '{"first_name":"Owner","last_name":"One","email":"owner@test","password":"pw"}' >/dev/null
OWNER_TOKEN=$(curl -s -X POST "$BASE_URL/auth/login" -H "Content-Type: application/json" \
  -d '{"email":"owner@test","password":"pw"}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')

# -- owner place to review --
OWNER_PLACE_ID=$(curl -s -X POST "$BASE_URL/places/" \
  -H "Authorization: Bearer $OWNER_TOKEN" -H "Content-Type: application/json" \
  -d '{"name":"ReviewTarget","city":"SJ","price_per_night":30}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
echo "OWNER_PLACE_ID=$OWNER_PLACE_ID"

# -- guest creates review (expect 201) --
REVIEW_ID=$(curl -s -X POST "$BASE_URL/reviews/" \
  -H "Authorization: Bearer $GUEST_TOKEN" -H "Content-Type: application/json" \
  --data-binary "{\"text\":\"Great stay\",\"place_id\":\"$OWNER_PLACE_ID\"}" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
echo "REVIEW_ID=$REVIEW_ID"

# GET review (200)
curl -i -s "$BASE_URL/reviews/$REVIEW_ID" | head -n 1

# -- intruder cannot edit (403) --
curl -s -X POST "$BASE_URL/users/" -H "Content-Type: application/json" \
  -d '{"first_name":"Intruder","last_name":"User","email":"intruder@test","password":"pw"}' >/dev/null
INTRUDER_TOKEN=$(curl -s -X POST "$BASE_URL/auth/login" -H "Content-Type: application/json" \
  -d '{"email":"intruder@test","password":"pw"}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')
curl -i -s -X PUT "$BASE_URL/reviews/$REVIEW_ID" \
  -H "Authorization: Bearer $INTRUDER_TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"text":"intruder edit"}' | head -n 1

# -- admin cannot edit (403) --
curl -i -s -X PUT "$BASE_URL/reviews/$REVIEW_ID" \
  -H "Authorization: Bearer $OWNER_TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"text":"admin edit"}' | head -n 1

# -- author can edit (200) --
curl -i -s -X PUT "$BASE_URL/reviews/$REVIEW_ID" \
  -H "Authorization: Bearer $GUEST_TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"text":"Edited by author"}' | head -n 1
curl -s "$BASE_URL/reviews/$REVIEW_ID" \
  | python3 -c 'import sys,json; print("text =", json.load(sys.stdin)["text"])'

# -- admin can delete (204), then 404 on fetch --
curl -i -s -X DELETE "$BASE_URL/reviews/$REVIEW_ID" \
  -H "Authorization: Bearer $OWNER_TOKEN" | head -n 1
curl -i -s "$BASE_URL/reviews/$REVIEW_ID" | head -n 1
