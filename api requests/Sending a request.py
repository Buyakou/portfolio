import requests

# URL for the request
url = "https://jsonplaceholder.typicode.com/posts"

# Data to send in JSON format
data = {
    "title": "foo",
    "body": "bar",
    "userId": 1
}

# Request headers
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer your_access_token"
}

# Sending a POST request with headers
response = requests.post(url, json=data, headers=headers)

# Displaying the results
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
