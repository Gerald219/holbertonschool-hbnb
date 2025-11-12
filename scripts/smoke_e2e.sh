#!/usr/bin/env bash
set -euo pipefail

BASE="http://127.0.0.1:5001/api/v1"

red()   { printf "\033[31m%s\033[0m\n" "$*"; }
green() { printf "\033[32m%s\033[0m\n" "$*"; }
fail()  { red "FAIL: $*"; exit 1; }

echo "== health =="
curl -fsS http://127.0.0.1:5001/ >/dev/null || fail "server not responding"
green "OK: server alive"

# seed users (ignore duplicate email errors)
curl -fsS -X POST "$BASE/users/" -H "Content-Type: application/json" \
  --data-binary '{"first_name":"Owner","last_name":"One","email":"owner@test","password":"pw"}' >/dev/null || true
curl -fsS -X POST "$BASE/users/" -H "Content-Type: application/json" \
  --data-binary '{"first_name":"Reviewer","last_name":"Two","email":"reviewer@test","password":"pw"}' >/dev/null || true

# tokens
OWNER_TOKEN=$(curl -fsS -X POST "$BASE/auth/login" -H "Content-Type: application/json" \
  --data-binary '{"email":"owner@test","password":"pw"}' | python3 -c 'import sys,json; print(json.load(sys.stdin)["access_token"])') || fail "owner login"
REVIEWER_TOKEN=$(curl -fsS -X POST "$BASE/auth/login" -H "Content-Type: application/json" \
  --data-binary '{"email":"reviewer@test","password":"pw"}' | python3 -c 'import sys,json; print(json.load(sys.stdin)["access_token"])') || fail "reviewer login"

# create place (owner)
PLACE_JSON=$(curl -fsS -X POST "$BASE/places/" -H "Authorization: Bearer $OWNER_TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"name":"Smoke Place","city":"SJ","price_per_night":99,"description":"smoke"}') || fail "create place"
PLACE_ID=$(printf "%s" "$PLACE_JSON" | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
[ -n "${PLACE_ID:-}" ] || fail "parse place id"
green "OK: place=$PLACE_ID"

# amenity (admin/owner)
AMENITY_JSON=$(curl -fsS -X POST "$BASE/amenities/" -H "Authorization: Bearer $OWNER_TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"name":"Wifi"}') || fail "create amenity"
AMENITY_ID=$(printf "%s" "$AMENITY_JSON" | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
[ -n "${AMENITY_ID:-}" ] || fail "parse amenity id"
green "OK: amenity=$AMENITY_ID"

# attach amenity
curl -fsS -X POST "$BASE/places/$PLACE_ID/amenities/$AMENITY_ID" -H "Authorization: Bearer $OWNER_TOKEN" >/dev/null || fail "attach amenity"
green "OK: amenity attached"

# reviewer creates one review
REVIEW_JSON=$(curl -fsS -X POST "$BASE/reviews/" -H "Authorization: Bearer $REVIEWER_TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"text":"first review ok","place_id":"'"$PLACE_ID"'"}') || fail "create review"
REVIEW_ID=$(printf "%s" "$REVIEW_JSON" | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
[ -n "${REVIEW_ID:-}" ] || fail "parse review id"
green "OK: review=$REVIEW_ID"

# negative: owner cannot review own place (expect 403)
code=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/reviews/" \
  -H "Authorization: Bearer $OWNER_TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"text":"owner self-review","place_id":"'"$PLACE_ID"'"}')
[ "$code" = "403" ] || fail "expected 403 for self-review, got $code"
green "OK: self-review blocked (403)"

# negative: duplicate review by same reviewer (expect 409)
code=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/reviews/" \
  -H "Authorization: Bearer $REVIEWER_TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"text":"dup","place_id":"'"$PLACE_ID"'"}')
[ "$code" = "409" ] || fail "expected 409 duplicate, got $code"
green "OK: duplicate blocked (409)"

# reviewer edits own review (200)
curl -fsS -X PUT "$BASE/reviews/$REVIEW_ID" -H "Authorization: Bearer $REVIEWER_TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"text":"edited by reviewer"}' >/dev/null || fail "reviewer edit"
green "OK: reviewer edit (200)"

# owner cannot edit reviewer’s review (403)
code=$(curl -s -o /dev/null -w "%{http_code}" -X PUT "$BASE/reviews/$REVIEW_ID" \
  -H "Authorization: Bearer $OWNER_TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"text":"owner tries edit"}')
[ "$code" = "403" ] || fail "expected 403 owner-edit, got $code"
green "OK: owner blocked editing others (403)"

# author deletes own review (204)
code=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$BASE/reviews/$REVIEW_ID" -H "Authorization: Bearer $REVIEWER_TOKEN")
[ "$code" = "204" ] || fail "expected 204 author delete, got $code"
green "OK: author delete (204)"

# recreate a review and admin delete (204)
R2=$(curl -fsS -X POST "$BASE/reviews/" -H "Authorization: Bearer $REVIEWER_TOKEN" -H "Content-Type: application/json" \
  --data-binary '{"text":"temp","place_id":"'"$PLACE_ID"'"}' | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])') || fail "recreate review"
code=$(curl -s -o /dev/null -w "%{http_code}" -X DELETE "$BASE/reviews/$R2" -H "Authorization: Bearer $OWNER_TOKEN")
[ "$code" = "204" ] || fail "expected 204 admin delete, got $code"
green "OK: admin delete (204)"

green "ALL GOOD: smoke_e2e passed"
