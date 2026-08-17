#!/bin/sh
# crude html -> text
tr '\n' ' ' < "$1" \
| sed 's/<script[^>]*>/\n@@SCRIPT@@/g; s/<\/script>/\n/g' \
| grep -v '^@@SCRIPT@@' \
| sed 's/</\n</g' \
| sed -n 's/^[^>]*>//p' \
| sed 's/&nbsp;/ /g; s/&amp;/\&/g; s/&lt;/</g; s/&gt;/>/g; s/&quot;/"/g; s/&#39;/'"'"'/g' \
| sed 's/^[[:space:]]*//; s/[[:space:]]*$//' \
| grep -v '^$'
