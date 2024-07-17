class Config:
    '''
    Do not change the name of this file.
    不要改动这个文件的名称。 
    '''
    '''
    IP and port of the server.
    服务器的IP和端口。
    '''
    #HOST = '192.168.3.187'
    HOST = '192.168.0.106'
    PORT = 9076
    '''
    Allows new account registration.
    开放账号注册。
    '''
    REGISTRATION = True
    '''
    SSL证书路径 - 留空则使用HTTP
    SSL certificate path. If left blank, use HTTP.
    '''
    SSL_CERT = ''  # *.pem
    SSL_KEY = ''  # *.key
    '''
    Flask default debug
    Flask内置Debug
    '''  
    DEBUG = True