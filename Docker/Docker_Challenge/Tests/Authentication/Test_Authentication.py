import os
import requests
# definition of the API address
api_address = 'framework_to_test'
# API port
api_port = 8000

# Request Alice
r = requests.get(
    url='http://{address}:{port}/permissions'.format(address=api_address, port=api_port),
    params= {
        'username': 'alice',
        'password': 'wonderland'
    }
)
output = '''
============================
    Authentication test
============================
request done at "/permissions"
| username="alice"
| password="wonderland"
expected result = 200
actual restult = {status_code}
==>  {test_status}
'''
# query status
status_code = r.status_code
# display the results
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(status_code=status_code, test_status=test_status))
# printing in a file
if os.environ.get('LOG') == '1':
    with open('/Results/api_test.log', 'a') as file:
        file.write(output.format(status_code=status_code, test_status=test_status))

# Request Bob
r = requests.get(
    url='http://{address}:{port}/permissions'.format(address=api_address, port=api_port),
    params= {
        'username': 'bob',
        'password': 'builder'
    }
)
output = '''
============================
    Authentication test
============================
request done at "/permissions"
| username="bob"
| password="builder"
expected result = 200
actual restult = {status_code}
==>  {test_status}
'''
# query status
status_code = r.status_code
# display the results
if status_code == 200:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(status_code=status_code, test_status=test_status))
# printing in a file
if os.environ.get('LOG') == '1':
    with open('/Results/api_test.log', 'a') as file:
        file.write(output.format(status_code=status_code, test_status=test_status))
        
# Request Clementine
r = requests.get(
    url='http://{address}:{port}/permissions'.format(address=api_address, port=api_port),
    params= {
        'username': 'clementine',
        'password': 'mandarine'
    }
)
output = '''
============================
    Authentication test
============================
request done at "/permissions"
| username="clementine"
| password="madarine"
expected result = 403
actual restult = {status_code}
==>  {test_status}
'''
# query status
status_code = r.status_code
# display the results
if status_code == 403:
    test_status = 'SUCCESS'
else:
    test_status = 'FAILURE'
print(output.format(status_code=status_code, test_status=test_status))
# printing in a file
if os.environ.get('LOG') == '1':
    with open('/Results/api_test.log', 'a') as file:
        file.write(output.format(status_code=status_code, test_status=test_status))