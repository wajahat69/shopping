import requests

response = requests.post(
    "https://hmb2ti6wa2h3gulbqn5vg2g32q0jubml.lambda-url.us-east-1.on.aws/",
    json={
        "httpMethod": "GET",
        "path": "/",
        "headers": {},
        "body": "",
        "isBase64Encoded": False
    }
)

print(response.status_code)
print(response.text)
