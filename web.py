from flask import Flask, render_template, request, flash, jsonify
from llm import embedding_persist, vector_search
from fastapi.encoders import jsonable_encoder
import os
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'lanwang/docs'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf'])
app.secret_key = 'ei1se13d'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(app.config['UPLOAD_FOLDER'] + '/' + filename)
            embedding_persist(app.config['UPLOAD_FOLDER'] + '/' + filename)
            flash('上传成功！', 'success')
        else:
            flash('只能上传txt和pdf类型文件！', 'false')
    file_list = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('upload.html', files=file_list)


@app.route('/search', methods=['POST'])
def search():
    # 获取传递的数据
    data = request.get_json()
    question = data['question']
    print(question)

    # 返回结果
    result = vector_search(question)
    
    return jsonify(json.dumps(jsonable_encoder(result), ensure_ascii=False))


if __name__ == '__main__':
    app.run(debug=True)
