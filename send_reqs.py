# -*- coding: utf-8 -*-
# Developer: Xianglin Wu (xianglin3092@gmail.com

import portalocker
import requests
import json

class Send_obj:
    def __init__(self, url=None, data=None):
        self.url = url
        self.data = data
        self.mode = ['get','post']

    def action(self, mode, url, data):
        '''
        The actions that "send" function can do.
        Input:
            mode: str
            url: str
            data: dict
        Output:
            req: dict
        '''
        if mode == 'get':
            req = requests.get(url, data)
        elif mode == 'post':
            req = requests.post(url, data)
        return req

    def send(self, mode, only_past=False):
        '''
        Send a get request. 
        If connection error exists, create a json file to save requests.
        If connection error is solved, send all the requests stored in json file.
        Input:
            only_past: bool
        Output:
            response_list: list of dict
            error_msg: str
        '''
        filename = 'send_data.json'
        if mode in self.mode:
            try:
                if only_past:
                    new_data = None
                else:
                    new_data = self.data
                
                send_data = self.write_file(mode, filename, new_data)

                if len(send_data) > 0:
                    response_list = []
                    for item in send_data:
                        req = self.action(mode=mode, url=self.url, data=item)
                        text = json.loads(req.text)
                        response_list.append(text)
                    self.clear_file(mode, filename)
                    return response_list
                else:
                    error_msg = 'No data can be sent.'
                    return error_msg
            
            except requests.exceptions.ConnectionError as error_msg:
                return error_msg
        else:
            return 'This function does not support this mode.'

    def write_file(self, mode, filename, new_data=None):
        '''
        Write & read the data which is prepared to send in a json file.
        input:
            filename: str
            new_data: dict
        output:
            data: list of dict
            file: json file
        '''
        try:
            with portalocker.Lock(filename, 'r') as jsonfile:
                input_data = json.load(jsonfile)
        
        except:
            input_data = dict( zip( self.mode , [ [] for i in range(len(self.mode)) ] ) )
        
        if new_data:
            with portalocker.Lock(filename, 'w') as jsonfile:
                if mode in input_data:
                    input_data[mode].append(new_data)
                else:
                    input_data[mode] = [new_data]
                
                json.dump(input_data, jsonfile)
        
        return input_data[mode]
    
    def clear_file(self, mode, filename):
        '''
        Clear all the content of a file.
        input:
            filename: str
        output:
            file: json file
        '''
        with portalocker.Lock(filename, 'r') as jsonfile:
                input_data = json.load(jsonfile)

        with portalocker.Lock(filename, 'w') as jsonfile:
            input_data[mode].clear()
            json.dump(input_data, jsonfile)


if __name__ == '__main__':
    # Example
    url = "http://127.0.0.1:5062"
    
    data1 = {"service":"sensor","operation":"get_config"}
    data2 = {"service":"sensor","operation":"add_sensor_information","sensor_id":"AAA01","status":"1"}
    
    ## Send a GET request
    test_1 = Send_obj(url, data1)
    get_1 = test_1.send('get')
    print(get_1)
    
    ## Send a POST request
    test_2 = Send_obj(url, data2)
    post_1 = test_2.send('post')
    print(post_1)
    
    ## Send a POST request (only the past request which is not sent)
    # test_3 = Send_obj(url)
    # post_2 = test_3.send('post', only_past=True)
    # print(post_2)

    ## Send a POST request and then send again (but only the past request which is not sent)
    # test_4 = Send_obj(url, data2)
    # post_3 = test_4.send('post')
    # post_4 = test_4.send('post', only_past=True)
    # print(post_4)
