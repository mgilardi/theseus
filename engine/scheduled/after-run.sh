#!/bin/bash
# When a run ends: the copies of Messages, Contacts and Mail go too. macOS protects the originals, but any app could read a copy left in this folder.
set -u
WS="${THESEUS_HOME:-$HOME/Theseus}"
cd "$WS" || exit 1
rm -f cache/chat-snapshot.db cache/contacts-*.db cache/mail-envelope.db cache/accounts.db
# A run can't delete its own scratch files, like a temporary copy of your Reminders.
rm -f exports/.*-tmp.json
exit 0
