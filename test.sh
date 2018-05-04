#!/bin/bash

curl -H "Content-Type: application/json" \
	-X POST \
	-d '{"content":{"email":"foo@bar.com"}}' \
 	https://api.monday.health/patient/referral/submit
