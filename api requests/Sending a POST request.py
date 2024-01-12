import requests

# URL for the POST request
url = "https://jsonplaceholder.typicode.com/posts"

# Data to send in JSON format
data = {
    "title": "foo",
    "body": "bar",
    "userId": 1
}

# Sending a POST request
response = requests.post(url, json=data)

# Displaying the results
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
