#!/bin/env bash

for filename in **/*.sql; do
    echo "Importing ${filename}"

    output="$(sqlite3 neat.db < "${filename}")"

    if [[ $? -ne 0 ]] ; then
        echo "Import failed with: ${output}"
    fi
done
