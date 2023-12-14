from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()


class GPTDriver:
  def __init__(self,
               resume_text):
    self.client = OpenAI()
    self.resume = resume_text # self.read_file(resume_file)
    self.prompts = {
      "candidate_name" : "I am providing you a piece of text. Please help me extract the name of candidate from the given text.Only write the name. The text is as follows:" + self.resume,
      "candidate_title" : "I am providing you a piece of text. Please help me extract the name of candidate job title from the given text.Only write the title.The text is as follows:" + self.resume,
      "work_experience" : "I am providing you a piece of text. Please help me extract work experience related details from the given text. Only specify the name of company, title of experience  and duration of each experience with respect to each company. Do not inidate work experience related details while listing the work experience related details. Please format it in bullet form. The text is as follows:" + self.resume,
      "projects" : "I am providing you a piece of text. Please help me extract only project related details from the given text. Do not indicate the duration, title and compnay name of each work experience. Please format it in bullet form. The text is as follows:" + self.resume,
      "skills" : "I am providing you a resume of candidate. Please help me extract top 10 technical skills listed on the given resume. The resume is as follows: " + self.resume,
      "career_summary" : "I am providing you a resume of candidate. Please help me extract career summary of the candidate mentioned on the given resume. Please summarize the result in three to four lines. The resume is as follows: " + self.resume,
      "education": "I am providing you a resume of candidate. Please help me extract qualification related details from the given resume. Only specify the name of educational institute, degree name and duration of each degree. Please write your response in bullet form by listing the name of degree and name of institute and duration in ; separated manner. The resume is as follows:" + self.resume
    }
    self.responses = {
      "candidate_name" : "",
      "candidate_title" : "",
      "work_experience" : "",
      "projects" : "",
      "skills" : "",
      "education": "",
      "career_summary": ""

    }

  @staticmethod
  def read_file(resume_file):
    with open(resume_file, 'r') as file:
      resume = file.readlines()
      resume = "".join(resume)
    return resume

  def invoke_chatgpt(self, prompt_key):
    response = self.client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": self.prompts[prompt_key]}
      ],
      temperature=0.2
    )
    self.responses[prompt_key] = response.choices[0].message.content
    print(f"{prompt_key} : {self.responses[prompt_key]}")


if __name__ == "__main__":
  gpt_driver = GPTDriver(resume_file="./output_text.txt")
  gpt_driver.invoke_chatgpt(prompt_key="education")
