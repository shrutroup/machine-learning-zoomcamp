import requests

# for testing lambda function on local machine
# url = 'http://localhost:8080/2015-03-31/functions/function/invocations'

# for testing lambda web service
url='https://1feyiqfvh1.execute-api.us-west-2.amazonaws.com/dev/predict'
request = {
   "url": 'https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg'
}

result = requests.post(url, json=request).json()
print(result)

# testing on the terminal using curl
# curl -X POST https://1feyiqfvh1.execute-api.us-west-2.amazonaws.com/dev/predict \
#   -H "Content-Type: application/json" \
#   -d '{"url": "https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg"}'