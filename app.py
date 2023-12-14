from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename  # Import secure_filename from werkzeug.utils
from preprocessor import Preprocessor
from chatgpt_driver import GPTDriver
from postprocessor import PostProcessor
import os

app = Flask(__name__)

class Driver:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.gpt_driver = None
        template_path = os.path.join(os.path.dirname(__file__), 'Template Resumes/template.docx')
        self.postprocessor = PostProcessor(template_docx_path=template_path)

    def document_converter(self, resume_path):
        resume_text = self.preprocessor.convert_docx_to_text(resume_path)
        self.gpt_driver = GPTDriver(resume_text=resume_text)
        self.gpt_driver.invoke_chatgpt(prompt_key="candidate_name")
        self.gpt_driver.invoke_chatgpt(prompt_key="candidate_title")
        self.gpt_driver.invoke_chatgpt(prompt_key="skills")
        self.gpt_driver.invoke_chatgpt(prompt_key="career_summary")
        self.gpt_driver.invoke_chatgpt(prompt_key="work_experience")
        self.gpt_driver.invoke_chatgpt(prompt_key="projects")
        self.gpt_driver.invoke_chatgpt(prompt_key="education")
        return self.gpt_driver.responses

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'resume' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['resume']

        if file.filename == '':
            return render_template('index.html', error='No selected file')

        if file:
            # Save the uploaded file in the same directory with a unique name
            filename = os.path.join(os.path.dirname(file.filename), secure_filename(file.filename))
            file.save(filename)

            driver = Driver()
            responses = driver.document_converter(resume_path=filename)

            # Generate a unique filename for the output file
            output_path = os.path.splitext(filename)[0] + '_output.docx'
            driver.postprocessor.write_doc(responses=responses, output_path=output_path)

            return send_file(output_path, as_attachment=True)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
