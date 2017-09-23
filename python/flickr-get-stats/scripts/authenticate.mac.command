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

# This macOS Finder command calls the peer name.sh script from the same folder.

script_path="$0"
if [[ "${script_path}" != /* ]]
then
  # Make relative path absolute.
  script_path="$(pwd)/$0"
fi

script_folder="$(dirname ${script_path})"
# echo $script_folder

script_name="$(basename $0)"
# echo "${script_name}"

script_base=$(echo "${script_name}" | sed -e 's/\(.*\)[.]mac[.]command/\1/')
# echo "${script_base}"

bash "${script_folder}/${script_base}.sh"
