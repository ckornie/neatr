#!/bin/env bash

for filename in *.txt; do
    tesseract "${filename}" "${filename%.txt}" pdf
done
