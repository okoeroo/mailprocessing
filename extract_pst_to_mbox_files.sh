#!/bin/bash

INPUT="$1"
OUTPUTDIR="$2"


if [ ! -f "${INPUT}" ]; then
    echo "No input file"
    echo "Use: <exec> <input pst file> <output directory>"
    exit 1
fi


if [ ! -d "${OUTPUTDIR}" ]; then
    echo "No output directory"
    exit 1
fi


# Read PST, 
# -j run multiple jobs,
# -D include deleted items
# -S output into split files
# -o results go into output directory
readpst \
    -j 4 \
    -D \
    -S \
    -o "${OUTPUTDIR}/" \
    "${INPUT}"

exit $?

