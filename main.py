from preprocessor import Preprocessor
from chatgpt_driver import GPTDriver
from postprocessor import PostProcessor

class Driver:
    def __init__(self):
        self.preprocesor = Preprocessor()
        self.gpt_driver = None
        self.postprocessor = PostProcessor(template_docx_path="../Template Resumes/template.docx")

    def document_coverter(self, resume_path):
        resume_text = self.preprocesor.convert_docx_to_text(resume_path)
        self.gpt_driver = GPTDriver(resume_text=resume_text)
        self.gpt_driver.invoke_chatgpt(prompt_key="candidate_name")
        self.gpt_driver.invoke_chatgpt(prompt_key="candidate_title")
        self.gpt_driver.invoke_chatgpt(prompt_key="skills")
        self.gpt_driver.invoke_chatgpt(prompt_key="career_summary")
        self.gpt_driver.invoke_chatgpt(prompt_key="work_experience")
        self.gpt_driver.invoke_chatgpt(prompt_key="projects")
        self.gpt_driver.invoke_chatgpt(prompt_key="education")
        self.postprocessor.write_doc(responses=self.gpt_driver.responses)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    driver = Driver()
    driver.document_coverter(resume_path="../Sample Resumes/Waseem-Haider.docx")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
