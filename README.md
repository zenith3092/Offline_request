# Offline_request

## Introduction
As we send a server a request, chances are some connection errors occur. This module can help you store sending data in a json file format first if you encounter some connection problems. After problems solved, you can activate this module again, and all the sending data stored in json file will be sent out.

## How to use?
### Step1: Creating url and sending data
#### Example:
```
url = "http://127.0.0.1:5062"
data = {"service":"business","operation":"get_main_data"}
```

### Step2: Defining a sending object
#### Example:
```
test = Send_obj(url, data)
```

### Step3: Call the method "send" and choose sending type
#### Example:
```
get = test.send('get')   # you can choose "get" or "post"
```

### Note:
If sending data have been stored in a json file and you want to send a server only past requests, you can insert the only_past in the method "send".
```
get2 = test.send('get', only_past=True)
```

