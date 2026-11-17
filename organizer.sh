#!/bin/bash
# This script is archives grades.csv with a timestamp, resets the workspace, and logs the action.

ARCHIVE_DIR="archive"
SOURCE="grades.csv"
LOG="organizer.log"

mkdir -p "$ARCHIVE_DIR"

if [ ! -f "$SOURCE" ]; then
    echo "Error: $SOURCE not found in $(pwd)" >&2
    exit 1
fi

TIMESTAMP=$(date +%Y%m%d-%H%M%S)
NEW_NAME="grades_${TIMESTAMP}.csv"

mv "$SOURCE" "$ARCHIVE_DIR/$NEW_NAME" || exit 1
: > "$SOURCE"

echo "[$TIMESTAMP] Archived: original=$SOURCE new=$ARCHIVE_DIR/$NEW_NAME" >> "$LOG"
echo "Archived $SOURCE -> $ARCHIVE_DIR/$NEW_NAME"
