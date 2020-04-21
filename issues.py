import requests
url = "https://api.github.com/repos/fahad-30/Snake.py/issues"

response = requests.request("GET",url)

# print(response.text)
response= response.json()

dict1 = response[0]
titles = dict1["title"] 

