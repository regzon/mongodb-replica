#!/usr/bin/env bash

set -mex

# If the primary host env variable is unset
# then we don't need to do primary host setup
if [ -z ${MONGO_PRIMARY_HOST+x} ]; then
    exec "$@"
fi

# Run the server in background
$@ &

echo "Connecting to the servers..."
until \
    mongo --host $MONGO_PRIMARY_HOST --eval "rs.status()" &&
    mongo --host $MONGO_SECONDARY_HOST1 --eval "rs.status()" &&
    mongo --host $MONGO_SECONDARY_HOST2 --eval "rs.status()"
do
  echo "Some of the servers haven't started yet, retrying..."
done
echo "Done"

echo "Setting up the primary server..."
mongo --host $MONGO_PRIMARY_HOST << EOF
rs.initiate({
  "_id":"rs0",
  "members":[
    {"_id":0,"host":"$MONGO_PRIMARY_HOST:27017"},
    {"_id":1,"host":"$MONGO_SECONDARY_HOST1:27017"},
    {"_id":2,"host":"$MONGO_SECONDARY_HOST2:27017"}
  ]
})
EOF
echo "Done"

# Return the server to foreground
fg
