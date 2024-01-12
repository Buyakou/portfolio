import requests

# URL for the GET request
url = "https://jsonplaceholder.typicode.com/posts/1"

# Sending a GET request
response = requests.get(url)

# Displaying the results
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
