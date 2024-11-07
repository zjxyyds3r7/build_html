# 前端快速部署

基于Python的flask框架与http.server的前端快速部署系统。作者：zjxyyds0307

上传格式：

​	一个zip压缩包，其根目录下包含index.html以及多个文件夹，无多余目录，如图。

<img src="static\样图.png" style="zoom:43%;" />

项目中共使用了两个端口：

- 上传和回调用端口，默认值为9999
- 展示端口，默认值为10000



项目使用10000端口挂载了一个简易的http.server服务器，通过继承SimpleHTTPRequestHandler实现了无法浏览根目录，只能浏览具体文件夹。

```python
class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<html><head><title>Home Page</title></head><body><h1>Welcome to the server!</h1><p>Please access other directories.</p></body></html>")
        else:
            super().do_GET()
```



项目使用9999端口挂载upload.html进行项目的上传，其中upload.html位于文件夹templates中 

项目压缩包上传完毕后，Python后端将把压缩包进行解压，解压路径为temp/当前时间/路径下。代码位于app.py line 34

```python
	# 获取上传的 HTML 项目文件
    project_file = request.files['project_file']

    # 保存文件到临时目录
    current_time = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    temp_dir = f'temp/{current_time}'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    project_path = os.path.join(temp_dir, project_file.filename)
    project_file.save(project_path)

    # 解压缩项目文件
    with zipfile.ZipFile(project_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
```

需要注意的是，Windows在解压中文文件时候会遇到乱码，原因是使用的解码方式不对，需要修改zipfile.py中的代码。

解压完毕后flask框架返回recall.html文件，通过jinja2模板将刚刚保存的url嵌入到html中。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>部署成功</title>
</head>
<body>
    <h1>部署成功</h1>
    <a href="{{ href }}">部署链接: {{ href }}</a>
</body>
</html>
```

最后点击recall.html中的超链接即可跳转到部署好的网页中。
