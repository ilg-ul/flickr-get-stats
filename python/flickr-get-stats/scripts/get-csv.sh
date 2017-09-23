#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# Safety settings (see https://gist.github.com/ilg-ul/383869cbb01f61a51c4d).

if [[ ! -z ${DEBUG} ]]
then
  set -x # Activate the expand mode if DEBUG is anything but empty.
fi

set -o errexit # Exit if command failed.
set -o pipefail # Exit if pipe failed.
set -o nounset # Exit if variable not set.

# Remove the initial space and instead use '\n'.
IFS=$'\n\t'

# -----------------------------------------------------------------------------

script_path="$0"
if [[ "${script_path}" != /* ]]
then
  # Make relative path absolute.
  script_path="$(pwd)/$0"
fi

script_folder="$(dirname ${script_path})"
# echo $script_folder

DEST_PATH="/Volumes/Second HD/Harlescu Library/Photos/Flickr/Statistics"

(cd "$(dirname "${script_folder}")/src"; caffeinate python -m ilg.flickr.statistics.get.csv --folder="${DEST_PATH}" --verbose | mail -s "flickr stats" ilg@livius.net)
