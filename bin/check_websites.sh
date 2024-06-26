#!/usr/bin/env bash
set -eu

LOGFILE=${1:-${HOME}/check_websites.log}
SLEEP=0

while getopts 'ds:' opt; do
  case $opt in
    d) LOGFILE=/dev/stdout;;
    s) SLEEP=$OPTARG;;
  esac
done
shift $((OPTIND-1))

websites='
https://expangea.com
https://app-test.expangea.com
https://imomdb.bii.a-star.edu.sg
https://karnanilab.com
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
    --sleep=$SLEEP \
    $websites

  echo
}

main "$@" &>>$LOGFILE

