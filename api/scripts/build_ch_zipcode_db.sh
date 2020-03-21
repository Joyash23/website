#/bin/sh

rm -f zipcodes.db
echo "CREATE TABLE zip_codes(code INTEGER)" | sqlite3 zipcodes.db
curl -v https://postleitzahlenschweiz.ch/tabelle/ 2>&1| egrep -o "<tr><td>[0-9]+" | egrep -o "[0-9]+"|\
    xargs -n1 -I% bash -c "echo 'INSERT INTO zip_codes VALUES(%)' |sqlite3 zipcodes.db"
