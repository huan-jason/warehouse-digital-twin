#!/usr/bin/env bash
set -eu

logfile=${1:-${HOME}/check_websites.log}

while getopts 'd' opt; do
  case $opt in
    d) logfile=/dev/stdout;;
  esac
done
shift $((OPTIND-1))

websites='
https://expangea.com
https://app-test.expangea.com
https://karnanilab.com
https://imomdb.bii.a-star.edu.sg
'
recipients='
jason.huan@tollgroup.com,
huan.jason@gmail.com
'

main() {
  date

  cd ${HOME}/digital-twin || exit 1

  docker compose exec app ./manage.py check_website \
    --verbose \
    --recipient "$recipients" \
    $websites
}

main "$@" &>>$logfile

