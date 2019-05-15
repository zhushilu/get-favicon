# 获取网站ico文件

借助google的api，实现在国内获取ico文件，主要是个人使用的一款开源网页书签系统中会对每个书签自动添加ico图表，google的国内无法使用，国内的其他ico获取服务又不稳定，所以用python简单的实现了一个。

## 使用方式

- 安装python环境
- 安装依赖包requirements.txt
- run(python app.py)

浏览器可直接访问：
```
http://127.0.0.1:8001/ico?url=http://github.com
```

第一次获取的时候会比较慢，因为要经过二次请求google，并本地缓存一份，第二次请求相同网站时就很快了。
