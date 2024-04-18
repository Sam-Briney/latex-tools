#!/bin/bash
#
# Generates a list of all the image files in a latex document $0
# Usage: ./list_images.sh main.tex >> .gitignore
# Pair this with .gitignore to avoid sending too many unused figures to overleaf
# Gitignore can look like:
# *.png
# *.pdf
# *.eps
#
# The above command will add exceptions to these global exclusions
#

grep -o {.*pdf $1 | sed 's/{/\n!/g'
grep -o {.*png $1 | sed 's/{/\n!/g'
grep -o {.*eps $1 | sed 's/{/\n!/g'
