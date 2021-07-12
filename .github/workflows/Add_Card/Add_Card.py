import requests
import issues
import sys

name = issues.titles
desc = issues.body
url = "https://api.trello.com/1/cards"
key = sys.argv[1]
# token = sys.argv[1]

query = {

'name':name,
'desc':desc,
'idList':'5e95c3a80d601f5535eb4259',
'key':key,
'token':'03341061d27ae05bb27b3e1c82beffb7b1472bd580c9b0631401773f2f007c80'
}

# headers ={ "Accept": "application/json"}

response = requests.request(
   "POST",
   url,
   params=query
)

print(response.text)
##'idList':'5e95c3a80d601f5535eb4259',
# 'name':'trial4',
# 'desc':'trial with jenkins',
