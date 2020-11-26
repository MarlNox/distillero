from flask import Flask
from flask import Flask, request, render_template, jsonify, redirect, make_response, url_for
import os
import logging
from logging import Formatter, FileHandler
from werkzeug.utils import secure_filename
import re
from summarizer import Summarizer
import textract
import nltk
from flask_dropzone import Dropzone
import os
from autocorrect import spell
from summa.summarizer import summarize as summy
from gensim.summarization import summarize as g_sumn
import textract
from transformers import *



app = Flask(__name__)


@app.route('/')



@app.route('/keyExt', methods=["GET"])
def keyword_extraction():
   return render_template('keyExt.html')


@app.route('/preproc', methods=["GET"])
def pre_process():
   return render_template('preproc.html')


@app.route('/summary', methods=["GET"])
def summar():
   return render_template('summary.html')


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'docx', 'docx', 'pptx', 'xls', 'xlsx', 'csv'])
dropzone = Dropzone(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DROPZONE_MAX_FILE_SIZE = 30,
#model = Summarizer()
d_tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-multilingual-cased')
d_model = DistilBertModel.from_pretrained('distilbert-base-multilingual-cased',output_hidden_states=True)

model = Summarizer(custom_model=d_model, custom_tokenizer=d_tokenizer)

_VERSION = 1  # API version


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS







@app.route("/keyword", methods=["GET", "POST"])
def keyword():
   text = request.form['text']
   word = nltk.word_tokenize(text)
   pos_tag = nltk.pos_tag(word)
   chunk = nltk.ne_chunk(pos_tag)
   NE = [" ".join(w for w, t in ele) for ele in chunk if isinstance(ele, nltk.Tree)]
   result = {
       "result": NE
   }
   result = {str(key): value for key, value in result.items()}
   return jsonify(result=result)


@app.route("/summarize", methods=["GET", "POST"])
def summarize():
   text = request.form['text'] 
   percent = request.form['percentage']
   #numri = request.form['numberOfWords']
   summare = text
   summare2 = str("'''" + summare + "'''")
   nr1 = float(percent)
   print(nr1)
   result1 = model(summare2, ratio=nr1)
   full = ''.join(result1)
   result = {"result": full}
   result = {str(key): value for key, value in result.items()}
   return jsonify(result=result)









@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        percent1 = request.form['percentage']
        percent = float(percent1)
        print(percent)
        file.save(os.path.join('./upload', file.filename))
        fls = file.filename
        filename, file_extension = os.path.splitext(fls)
        if file_extension == 'pdf':
            if file and allowed_file(file.filename):
                summare = textract.process('./upload/'+fls, method='pdftotext').decode('utf-8')
                summare2 = str("'''" + summare + "'''")
                print(percent)
                print(summare2)
                result = model(summare2, ratio=percent)
                full = ''.join(result)
                return jsonify({"output": full})
        else:
            if file and allowed_file(file.filename):
                summare = textract.process('./upload/' + fls).decode('utf-8')
                summare2 = str(" ''' " + summare + "'''")
                result = model(summare2, ratio=percent)
                full = ''.join(result)
                return jsonify({"output": full})

    elif request.method == 'GET':
            return render_template('upload.html')
    else:
            return jsonify({"error": "Please try a new file."})


#
# @app.errorhandler(500)
# def internal_error(error):
#     print(str(error))  # ghetto logging
#
#
# @app.errorhandler(404)
# def not_found_error(error):
#     print(str(error))
#
#
# @app.errorhandler(405)
# def not_allowed_error(error):
#     print(str(error))
#
# if not app.debug:
#     file_handler = FileHandler('error.log')
#     file_handler.setFormatter(
#         Formatter('%(asctime)s %(levelname)s: \
#             %(message)s [in %(pathname)s:%(lineno)d]')
#     )
#     app.logger.setLevel(logging.INFO)
#     file_handler.setLevel(logging.INFO)
#     app.logger.addHandler(file_handler)
#     app.logger.info('errors')
#
#


if __name__ == '__main__':
    app.run(debug=True)

