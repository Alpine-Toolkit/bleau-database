####################################################################################################

user='fabrice'
password='fabricebleau'

host="127.0.0.1:8000"
endpoint="/api/circuit/2452/"
url="http://${host}${endpoint}"

json="@post.json"

####################################################################################################

# Get
# curl -H 'Accept: application/json; indent=4' -u ${user}:${password} ${url}

# Create
# curl -XPOST -H "Content-type: application/json" --data "${json}" -u ${user}:${password} ${url}

# Partial Update
# curl -XPATCH -H "Content-type: application/json" --data "${json}" -u ${user}:${password} ${url}

# Update
# curl -XPUT -H "Content-type:application/json" --data "${json}" -u ${user}:${password} ${url}

# Delete
# curl -XDELETE -u ${user}:${password} ${url}

####################################################################################################
#
# End
#
####################################################################################################
