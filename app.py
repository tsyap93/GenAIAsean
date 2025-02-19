import streamlit as st
import requests
import re
import os
from langchain_community.document_loaders import PyPDFLoader
from typing import Optional
import urllib.request
import urllib.parse
import json
from dotenv import load_dotenv
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv()
ibm_api_key = os.getenv("IBM_API_KEY", None)

st.set_page_config(
    page_title="HireHero",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded")

# table with evaluations, to be included in UI
# df = pd.read_excel("resume_review.xlsx"
# )

sorted_result = []

# Define the URL
url = 'https://iam.cloud.ibm.com/identity/token'

# Define the data
data = {
    'grant_type': 'urn:ibm:params:oauth:grant-type:apikey',
    'apikey': ibm_api_key  
}

# Encode the data
data = urllib.parse.urlencode(data).encode()

# Create the request object
req = urllib.request.Request(url, data=data, method='POST')

# Make the request and read the response
with urllib.request.urlopen(req) as response:
    response_data = response.read().decode('utf-8')

current_token = json.loads(response_data)["access_token"]

headers = {
	"Accept": "application/json",
	"Content-Type": "application/json",
	"Authorization": "Bearer " + current_token
}

url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"

def send_to_model(prompt):

    body = {
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": 500,
            "min_new_tokens": 0,
            "repetition_penalty": 1
        },
        "model_id": "meta-llama/llama-3-3-70b-instruct",
        "project_id": "<Project ID>"
    }

    response = requests.post(
        url,
        headers=headers,
        json=body
    )

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    generated_text = data['results'][0]['generated_text']
    matches = re.findall(r"\{[^}]+\}", generated_text)
    score_dict = json.loads(matches[0])

    return score_dict

def pdf_to_text(path: str,
                start_page: int = 1,
                end_page: Optional[int | None] = None) -> list[str]:
  """
  Converts PDF to plain text.

  Args:
      path (str): Path to the PDF file.
      start_page (int): Page to start getting text from.
      end_page (int): Last page to get text from.
  """
  loader = PyPDFLoader(path)
  pages = loader.load()
  total_pages = len(pages)

  if end_page is None:
      end_page = len(pages)

  text_list = []
  for i in range(start_page-1, end_page):
      text = pages[i].page_content
      text = text.replace('\n', ' ')
      text = re.sub(r'\s+', ' ', text)
      text_list.append(text)

  return text_list

def assess_cv(cv, requirements):
     
    prompt = '''System: Assess the CV based on the job requirements below. Score the CV out of 10 on how suitable is the candidate. Give justifications for the score.
    Output must be in valid JSON like the following example /{/{"score": 3, "justification": "This candidate is not suitable as he does not know python which is a key requirement."/}/}. Output must include only JSON.
      '''
    prompt += "input: \n\n"
    prompt += "CV: " + " ".join(cv)

    prompt += "Requirements:" +  " ".join(requirements) + "\n\n output: \n"

    return(send_to_model(prompt))

with st.sidebar:
    st.title("""💼  HireHero - AI Interview Scheduler""")

    #upload job description
    uploaded_files_jd = st.file_uploader(
    "Job Description Upload", accept_multiple_files=True
    )

    jd_text = ""

    for file_jd in uploaded_files_jd:
        st.write("filename:", file_jd.name)
        with open("temp_save", 'wb') as f: 
            f.write(file_jd.getvalue())
        jd_text = pdf_to_text("temp_save")

    #upload resumes
    uploaded_files_resume = st.file_uploader(
    "Bulk Resume Upload", accept_multiple_files=True
    )

    candidate_resume=[]
    for resume in uploaded_files_resume:
        st.write("filename:", resume.name)
        with open("temp_save", 'wb') as f: 
            f.write(resume.getvalue())

        resume_text = pdf_to_text("temp_save")
        score_dict = assess_cv(resume_text, jd_text)
        score_dict["filename"] = resume.name
        sorted_result.append(score_dict)
sorted_result= sorted(sorted_result, key=lambda x: x["score"], reverse=True)

# Resume Summary of Selected Resumes
st.markdown('### Resume Reviews')
# st.table(df)
display_contacts=[]
st.write("Below are the assessment results, sorted by highest score:")
for idx, item in enumerate(sorted_result, start=1):
    if item['score']<7:
        continue
    st.subheader(f"Candidate #{idx}")
    st.write(f"**Filename**: {item['filename']}")
    st.write(f"**Score**: {item['score']}")
    st.write(f"**Justification**: {item['justification']}")
    st.write("---")
    display_contacts.append(item['filename'])

#sorted_filenames = [item["filename"] for item in sorted_result]
# Selecting Resumes
st.markdown('### Resume Selection for Interview Scheduling')
options = st.multiselect(
    "Select the shortlisted candidates",
    display_contacts
)

if st.button("Send Invites"):
    #add the send invite action over here
    st.write("Meeting invites have been drafted.")