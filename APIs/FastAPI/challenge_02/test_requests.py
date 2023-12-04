import requests
import time
from multiprocessing import Pool

if __name__ == '__main__':
    response = requests.get(url='http://127.0.0.1:8000/getMCQ?use=Positioning%20test&quantity=10&subjects=Databases',
                            headers={'credentials': 'basis alice:wonderlan'})
    print(response.status_code)