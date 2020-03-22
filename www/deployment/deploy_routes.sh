#!/bin/sh
LANGS="www en de fr it"
for lang in $LANGS
do
    DOMAIN=$lang envsubst < route.yaml | oc apply -f -
done
