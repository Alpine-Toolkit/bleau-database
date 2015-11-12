./bin/importer --rewrite=test.json data/bleau.json
rc=$(diff -q test.json data/bleau.json)
if [ -n -$rc- ]; then
  echo
  echo Any changes to bleau.json
else
  diff -Naur test.json data/bleau.json | less
fi

