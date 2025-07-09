from flask import Flask, render_template, redirect, request, session, flash
from werkzeug.utils import secure_filename
import ai
import os
import base64

app = Flask(__name__)

app.secret_key = os.getenv("SECRET_KEY")
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER")
IMAGE_FOLDER = os.getenv("IMAGE_FOLDER")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'webp'}

# checks for the valid file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# converts image file into base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def handle_pdf_upload(message=None, document):
    filename = secure_filename(document.filename)
    document_path = os.path.join(UPLOAD_FOLDER, filename)
    document.save(document_path)            
    
    file_id=ai.upload_file(document_path)
                
    # file is uploaded first time, get the file_id and save it in session
    if file_id:
        session['uploaded_file_id'] = file_id
        session.modified = True                     
                
    # user also sends message with file
    if file_id and message:                    
        return ai.get_response(message,file_id)                
    # only file uploaded and no question
    else:
        prompt = "If this document is about space give a summary for this document in 5 lines, \
                    else tell this is not relevant to the subject"
        return ai.get_response(prompt, file_id)

def handle_image_upload(message=None, document, file_ext):
    filename = secure_filename(document.filename)
    image_path = os.path.join(IMAGE_FOLDER, filename)
    document.save(image_path)                
    base64_image = encode_image(image_path)     
    
    if message:
        return ai.image_upload(question, base64_image, file_ext)
    else:
        prompt = "Tell me what this image is about. And if its unrelated to space say its unrelevant to the topic"
        return ai.image_upload(prompt, base64_image, file_ext)        
            
               
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'history' not in session:
        session['history'] = []
        
    if request.method == 'POST':
        message=request.form.get('question')
        document = request.files('doc_file')
                
        # if user uploads file for the first time
        if document and allowed_file(document.filename):                        
            file_ext = (document.filename).rsplit('.', 1)[1].lower()             
            
            if file_ext == "pdf":
                answer = handle_pdf_upload(message, document)                           
            elif file_ext in {'png', 'jpg', 'jpeg', 'webp'}:
                answer = handle_image_upload(message, document, file_ext)
            else:
                flash("Unsupported file type")  
                return redirect('/')                                          

        # file  already uploaded + ask questions about it    
        elif 'uploaded_file_id' in session and message :            
            file_id =  session['uploaded_file_id']
            answer = ai.get_response(message, file_id)   
                        
        # Only text input    
        elif  message:
            answer = ai.message_only(message)                                      
        
        else:        
            flash("Please upload a file or ask a question.")
            return redirect('/')
    
    return render_template('index.html', history=session.get('history', []))
    
if __name__ == "__main__":
    app.run(debug = True)
