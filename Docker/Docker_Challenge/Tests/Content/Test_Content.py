import os
import requests
import math
# definition of the API address
api_address = 'framework_to_test'
# API port
api_port = 8000

# Request I Alice
r = requests.get(
    url='http://{address}:{port}/v1/sentiment'.format(address=api_address, port=api_port),
    params= {
        'username': 'alice',
        'password': 'wonderland',
        'sentence': 'life is beautiful'
    }
)

output = '''
============================
    Content test
============================
request done at "/v1/sentiment"
| username="alice"
| password="wonderland"
| sentence="life is beautiful"
expected result = positive score
actual result = {score}
status = {status_code}
==>  {test_status}
'''
# query status
status_code = r.status_code
score = r.json()["score"]
# display the results
if score >= 0:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(score = score, status_code=status_code, test_status=test_status))
# printing in a file
if os.environ.get('LOG') == '1':
    with open('/Results/api_test.log', 'a') as file:
        file.write(output)

# Request II Alice
r = requests.get(
    url='http://{address}:{port}/v2/sentiment'.format(address=api_address, port=api_port),
    params= {
        'username': 'alice',
        'password': 'wonderland',
        'sentence': 'that sucks'
    }
)
output = '''
============================
    Content test
============================
request done at "/v2/sentiment"
| username="alice"
| password="wonderland"
| sentence="that sucks"
expected result = negative score
actual result = {score}
status = {status_code}
==>  {test_status}
'''
# query status
status_code = r.status_code
score = r.json()["score"]
# display the results
if score < 0:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(score = score, status_code=status_code, test_status=test_status))
# printing in a file
if os.environ.get('LOG') == '1':
    with open('/Results/api_test.log', 'a') as file:
        file.write(output)