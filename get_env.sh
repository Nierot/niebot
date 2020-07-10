#!/bin/sh
echo "BOT_TOKEN = $TOKEN"
echo "OWNER_ID = $OWNER_ID"

echo "class Secrets()" >> secrets.py
echo "    def __init__(self):" >> secrets.py
echo "        self.BOT_TOKEN=$TOKEN" >> secrets.py
echo "        self.OWNER_ID=$OWNER_ID" >> secrets.py

cat secrets.py