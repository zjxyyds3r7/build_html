import datetime
import time
import zipfile

from flask import Flask, request
from flask import render_template

from getrun import *

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("upload.html")


OutPort = 10000


class delFile(threading.Thread):
    def __init__(self, path):
        threading.Thread.__init__(self)
        self.path = path

    def run(self):
        time.sleep(30)
        os.remove(self.path)


@app.route('/deploy', methods=['POST'])
def deploy():
    global OutPort
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

    delFile(project_path).start()
    url = ':'.join(request.host_url.split(':')[:-1])

    return render_template('recall.html', href=f'{url}:{OutPort}/{current_time}')


if __name__ == '__main__':
    # ReNginx().start()
    runHttp(OutPort, 'temp').start()
    app.run(port=9999, host='0.0.0.0')
