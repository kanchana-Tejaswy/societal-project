import requests

def test_upload():
    url = "http://127.0.0.1:5000/add"
    data = {'plastic_type': 'PET', 'quantity': '12'}
    files = {'image': open('test.jpg', 'rb')}
    
    res = requests.post(url, data=data, files=files, allow_redirects=False)
    print(f"Status: {res.status_code}")
    print(f"Redirected to: {res.headers.get('Location')}")

if __name__ == "__main__":
    test_upload()
