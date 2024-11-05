#!/bin/sh

sudo docker compose -f firefox-hub.yml up --scale firefox=1
