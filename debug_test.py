#!/usr/bin/env python3

import requests
import json

# Test the specific question
question = "how many interview rounds I have to give in this interview"
print(f"Testing question: {question}")

# Send the request
response = requests.post(
    "http://localhost:8080/api/chat/message",
    json={"message": question}
)

print(f"Status Code: {response.status_code}")
print(f"Response: {response.text}")

# Parse the response
if response.status_code == 200:
    data = response.json()
    print(f"\nParsed Response:")
    print(f"Message: {data.get('message')}")
    print(f"Response: {data.get('response')}")
    print(f"Source: {data.get('source')}")
    print(f"Timestamp: {data.get('timestamp')}")
else:
    print(f"Error: {response.text}")
