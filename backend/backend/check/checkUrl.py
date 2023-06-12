from django.urls import resolve
try:
    resolve('http://localhost:8000/api/login/')
    # URL tồn tại
    print("URL exists")
except:
    # URL không tồn tại
    print("URL does not exist")