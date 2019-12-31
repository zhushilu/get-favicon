from flask import Flask,request,send_file
import requests
from io import BytesIO
import os
import re
import config

from flask import render_template

app = Flask(__name__)
app.config.from_object(config)

favicon_server='https://favicon.zhusl.com/?url='
#favicon_server='http://www.google.com/s2/favicons?domain='

# 移除字符串开头的多个字符
def strip2(s, chars):
    re_chars = re.escape(chars)
    s = re.sub(r'^(?:%s)+(?P<right>.*)$' % re_chars, '\g<right>', s)
    s = re.sub(r'^(?P<left>.*?)(?:%s)+$' % re_chars, '\g<left>', s)
    return s

def get_url(url):
    response=requests.get(url)
    data = response.content
    return data

def static_list():
    ico_dir = {}
    list_dir = os.listdir('static')
    for  i in list_dir:
        if i[-3:] == 'ico':
            ico_dir[i[0:-4]] = i
    return ico_dir


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/icolist')
def ico_list():
    ico_dict = static_list()
    print(ico_dict)
    return render_template('index.html',ico_dict = ico_dict)
    #return str(ico_dict)


## 获取网站favicon的api，请求方式（百度：'http://xxxx:xx/favicon/baidu.com'）
@app.route('/favicon/<url>', methods=['GET'])
def res_favicon(url):
    res = requests.get(favicon_server+url)
    data = res.content
    header = res.headers
    print(header)
    url_ico_b = BytesIO(data)
    return send_file(url_ico_b,attachment_filename='favicon.ico', mimetype='image/x-icon')


@app.route('/ico', methods=['GET'])
def get_favicon():
    x = request.args.get('url')
    y = strip2(x,'http://')
    z = strip2(y,'https://')
    url_strip = z.split('/')[0]
    print(url_strip)
    if os.path.exists('./static/'+url_strip+'.ico'):
        print('ico is exist')
        with open('./static/'+url_strip+'.ico','rb') as f:
            url_ico = f.read()
            url_ico_b = BytesIO(url_ico)
            return send_file(url_ico_b,attachment_filename='favicon.ico', mimetype='image/x-icon')
    else:
      print('ico is not exist')
      res = get_url(favicon_server+url_strip)
      with open('./static/'+url_strip+'.ico','wb') as f:
          f.write(res)
          f = BytesIO(res)
          return send_file(f,attachment_filename='favicon.ico', mimetype='image/x-icon')


if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8001')
