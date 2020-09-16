from flask import Flask
from flask import Flask, request, render_template, jsonify, redirect, make_response, url_for
import nltk
import os
from flask_dropzone import Dropzone
from autocorrect import spell
from summa.summarizer import summarize as summy
from gensim.summarization import summarize as g_sumn
import textract
import nltkk
import pdf2txt
import logging
from logging import Formatter, FileHandler
from werkzeug.utils import secure_filename


app = Flask(__name__)


@app.route('/')
@app.route('/keyExt', methods=["GET"])
def keyword_extraction():
    return render_template('keyExt.html')


@app.route('/preproc', methods=["GET"])
def pre_process():
    return render_template('preproc.html')


@app.route('/summary', methods=["GET"])
def summary():
    return render_template('text_Summarization.html')


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
    text1 = request.form['text']
    s2 = "&tty&80*123408&&&xxcc&&vvbb&&&&324562jjkb@#_!+*&$)@NQB("
    s3 = "jcewfrnnc2@@@#328&!%#&!@*$(*)(@#^$(!&$**#^^$"

    numri1 = text1.partition(s3)[2]
    numri = int(numri1 or 0)
    if numri == 0:
        lngth1 = text1.partition(s2)[2]
        lngth = float(lngth1)
        textx = text1.partition(s2)[0]
        textu = str(textx)
        b_list = textu.split()
        text = " ".join(b_list)
        sent = nltk.sent_tokenize(text)
        if len(sent) < 2:
            summary1 = "please pass more than 3 sentences to summarize the text"
        else:
            r = lngth
            summary = summy(text, ratio=r)

            summ = nltk.sent_tokenize(summary)
            summary1 = (" ".join(summ[:2]))
            result = {
                "result": summary1
            }
            result = {str(key): value for key, value in result.items()}
            return jsonify(result=result)
    else:
        numri1 = text1.partition(s3)[2]

        numri = int(numri1 or 0)

        textx = text1.partition(s2)[0]
        textu = str(textx)
        b_list = textu.split()
        text = " ".join(b_list)
        sent = nltk.sent_tokenize(text)
        if len(sent) < 2:
            summary1 = "please pass more than 3 sentences to summarize the text"
        else:
            print(numri)
            t = numri
            summary = summy(text, words=numri)
            summ = nltk.sent_tokenize(summary)
            summary1 = (" ".join(summ[:2]))
            result = {
                "result": summary1
            }
            result = {str(key): value for key, value in result.items()}
            return jsonify(result=result)


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['pdf', 'pptx', 'xlsx', 'docx', 'txt'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DROPZONE_MAX_FILE_SIZE = 30,

_VERSION = 1  # API version


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('preproc.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename, file_extension = os.path.splitext('/path/to/somefile.ext')

        if file_extension == "pdf":
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                path = "./uploads/{}".format(filename)
                print("file was uploaded in {} ".format(path))
                myfile1 = textract.process("./uploads/{}".format(filename), method='pdfminer').decode('utf-8')
                a_list = myfile1.split()
                myfile2 = " ".join(a_list)
                print(myfile2)
                summare = summy(myfile2)
                summe = nltk.sent_tokenize(summare)
                summare1 = (" ".join(summe[:2]))
                summare2 = str(summare1)
                return jsonify({"output": summare2})
            else:
                return ('', 204)
        else:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                path = "./uploads/{}".format(filename)
                print("file was uploaded in {} ".format(path))
                myfile1 = textract.process("./uploads/{}".format(filename)).decode('utf-8')
                a_list = myfile1.split()
                myfile2 = " ".join(a_list)
                print(myfile2)
                summare = summy(myfile2)
                summe = nltk.sent_tokenize(summare)
                summare1 = (" ".join(summe[:2]))
                summare2 = str(summare1)
                return jsonify({"output": summare2})
            else:
                return ('', 204)
    elif request.method == 'GET':
        return render_template('dropimage.html')
    else:
        return jsonify({"error": "Please try a new file."})


@app.route('/form', methods=['POST'])
def handle_form():
    title = request.form.get('title')
    return 'file uploaded and form submit<br>title: %s<br> description: %s' % (title, description)


#
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

