from flask import Flask, request, render_template
from flask.globals import session
import time, telepot, os,fnmatch

app = Flask(__name__ , static_url_path="/images",static_folder=".\\app\\Static\\images")
app.secret_key='123456789'


@app.route('/',methods=['GET'])
def Service_Start():
    if(session.get('Admin')):
        templ = render_template('index.html')
    else:
        templ = render_template('index.html')
    return templ

@app.route('/send_file',methods=['POST'])
def send_File():
    Admin = {'PATH_FILES':'','TOKEN':'','CHAT_ID':''}
    PATH_FILES = request.form.get('Th_path_Files')
    TOKEN = request.form.get('Th_Token')  
    CHAT_ID = request.form.get('Th_chat_ID')  
    
    Admin['PATH_FILES'] = PATH_FILES
    Admin['TOKEN'] = TOKEN
    Admin['CHAT_ID'] = CHAT_ID
    session['Admin'] = Admin
    bot = telepot.Bot(TOKEN)
    while True:
        for file in os.listdir(PATH_FILES):
            if not(fnmatch.fnmatch(file, '*_done.*')):
                full_file = os.path.join(PATH_FILES, file)
                bot.sendDocument(chat_id=CHAT_ID,document=open(full_file,'rb'))
                file_split = file.split('.')
                new_name = f'''{file_split[0]}_done.{file_split[1]}'''
                full_new_file = os.path.join(PATH_FILES,new_name)
                os.rename(full_file,full_new_file)
        time.sleep(3600)



