import streamlit as st
import urllib.parse
import webbrowser
from interview_scheduler_for_top_candidates import interview_scheduler

st.title("Automated Interview Invitation Emails")

# Example summaries list
summaries_list =[
    {
        "summary": "Arjun Patel is a highly experienced Data Scientist with over 5 years in the field, specializing in designing and implementing advanced analytics models and algorithms to solve complex business problems. His proficiency in Python, R, and SQL, coupled with his hands-on experience with machine learning frameworks like TensorFlow, Keras, PyTorch, and scikit-learn, has enabled him to lead and deliver multiple successful projects. Arjun has a strong background in big data technologies, having worked extensively with Hadoop and Spark, and is adept at utilizing cloud platforms such as AWS and Azure for scalable solutions. His educational background includes a Master's degree in Computer Science from the University of Mumbai, and he holds certifications as an AWS Solutions Architect. Arjun's notable achievements include developing predictive models that improved business decision-making processes and presenting his findings in a clear, compelling manner to both technical and non-technical stakeholders. He is located in Mumbai and can be reached at arjun.patel@example.com.",
        "location": "Mumbai",
        "email": "arjun.patel@example.com"
    },
    {
        "summary": "Samantha Lee is a seasoned Data Scientist with 6 years of experience in analyzing large, complex datasets to identify trends and provide actionable insights. She excels in developing and deploying machine learning models using Python, R, SQL, and advanced frameworks such as TensorFlow, Keras, PyTorch, and scikit-learn. Samantha has successfully led projects on predictive modeling, data visualization using Tableau and Power BI, and has a keen eye for data preprocessing to ensure quality and integrity. She holds a Master's degree in Statistics from the Indian Institute of Technology (IIT) Bangalore and is an AWS Certified Developer. Samantha is known for her strong analytical, problem-solving, and communication skills, enabling her to work effectively in fast-paced environments and manage multiple projects simultaneously. She has also contributed to industry conferences as a speaker on data science topics. Samantha is based in Bangalore and can be contacted at samantha.lee@example.com.",
        "location": "Bangalore",
        "email": "samantha.lee@example.com"
    },
    {
        "summary": "Rahul Kumar is a proficient Data Scientist with 4 years of hands-on experience in machine learning, data analysis, and data visualization. He has a robust understanding of Python, R, SQL, and has implemented machine learning models using frameworks such as TensorFlow, Keras, PyTorch, and scikit-learn. Rahul has worked on several high-impact projects involving big data technologies like Hadoop and Spark, and has leveraged cloud platforms such as AWS and Google Cloud for efficient data processing. He holds a Master's degree in Information Technology from the University of Hyderabad and is certified in Google Data Analytics. Rahul is skilled in presenting data-driven insights to diverse audiences, ensuring that his findings drive business growth and innovation. He is located in Hyderabad and can be reached at rahul.kumar@example.com.",
        "location": "Hyderabad",
        "email": "rahul.kumar@example.com"
    },
    {
        "summary": "Maya Reddy is an accomplished Data Scientist with 7 years of extensive experience in statistical analysis, machine learning, and big data technologies. She is proficient in Python, R, SQL, and has hands-on experience with machine learning frameworks such as TensorFlow, Keras, PyTorch, and scikit-learn. Maya has led numerous projects on data visualization using Tableau and Power BI, and has a proven track record of working with cloud platforms like AWS and Azure. She holds a Master's degree in Mathematics from the Indian Institute of Technology (IIT) Delhi and is certified as a Google Cloud Professional Data Engineer. Maya has been instrumental in mentoring junior data scientists and promoting best practices in data science methodologies. She is located in Delhi and can be contacted at maya.reddy@example.com.",
        "location": "Delhi",
        "email": "maya.reddy@example.com"
    },
    {
        "summary": "John Smith is a dedicated Data Scientist with 5 years of experience in machine learning, statistical modeling, and data analysis. He is proficient in Python, R, SQL, and has a strong command of machine learning frameworks like TensorFlow, Keras, PyTorch, and scikit-learn. John has successfully led projects involving big data technologies like Hadoop and Spark, and has hands-on experience with cloud platforms such as AWS and Azure. He holds a Master's degree in Computer Science from the University of Pune and is certified as a Microsoft Azure Data Scientist Associate. John's analytical prowess and effective communication skills have enabled him to translate complex data insights into strategic business recommendations. He is located in Pune and can be reached at john.smith@example.com.",
        "location": "Pune",
        "email": "john.smith@example.com"
    },
    {
        "summary": "Priya Sharma is an insightful Data Scientist with over 4 years of experience in transforming raw data into meaningful insights. She is proficient in Python, R, SQL, and has expertise in machine learning frameworks such as TensorFlow, Keras, PyTorch, and scikit-learn. Priya has led projects on predictive modeling, data visualization using Tableau and Power BI, and data preprocessing to ensure data quality and integrity. She holds a Master's degree in Statistics from the University of Delhi and is certified in Google Data Analytics. Priya's ability to collaborate with cross-functional teams and her passion for data-driven decision-making make her a valuable asset. She is located in Gurgaon and can be contacted at priya.sharma@example.com.",
        "location": "Gurgaon",
        "email": "priya.sharma@example.com"
    },
    {
        "summary": "Ankit Mehta is an innovative Data Scientist with 5 years of experience in building and deploying scalable machine learning models. He is proficient in Python, R, SQL, and has hands-on experience with frameworks like TensorFlow, Keras, PyTorch, and scikit-learn. Ankit has led projects involving big data technologies like Hadoop and Spark, and has expertise in utilizing cloud platforms such as AWS and Azure. He holds a Bachelor's degree in Computer Science from the Indian Institute of Technology (IIT) Bombay and is certified in AWS Certified Data Analytics - Specialty. Ankit's contributions to AI conferences and published research papers highlight his commitment to advancing the field. He is based in Ahmedabad and can be reached at ankit.mehta@example.com.",
        "location": "Ahmedabad",
        "email": "ankit.mehta@example.com"
    },
    {
        "summary": "Ayesha Khan is a strategic Data Scientist with 6 years of experience in analyzing business processes and implementing data-driven strategies. She is proficient in Python, R, SQL, and has expertise in machine learning frameworks such as TensorFlow, Keras, PyTorch, and scikit-learn. Ayesha has led projects on data visualization using Tableau and Power BI, and has worked with big data technologies like Hadoop and Spark. She holds an MBA from the Indian School of Business (ISB) Hyderabad and is certified in Lean Six Sigma. Ayesha's strong analytical skills and business acumen have enabled her to drive operational efficiency and improve customer experiences. She is located in Kolkata and can be contacted at ayesha.khan@example.com.",
        "location": "Kolkata",
        "email": "ayesha.khan@example.com"
    },
    {
        "summary": "Vikram Singh is a distinguished Data Scientist with 7 years of experience in statistical analysis, machine learning, and big data technologies. He is proficient in Python, R, SQL, and has hands-on experience with machine learning frameworks such as TensorFlow, Keras, PyTorch, and scikit-learn. Vikram has led projects involving predictive analytics and recommendation systems, and has worked with cloud platforms such as AWS and Azure. He holds a Ph.D. in Data Science from the Indian Institute of Technology (IIT) Madras and is certified as a Microsoft Azure Data Scientist Associate. Vikram's research contributions and industry white papers underscore his expertise. He is based in Bangalore and can be reached at vikram.singh@example.com.",
        "location": "Bangalore",
        "email": "vikram.singh@example.com"
    },
    {
        "summary": "Neha Gupta is a meticulous Data Scientist with 5 years of experience in designing and maintaining data pipelines. She is proficient in Python, R, SQL, and has expertise in machine learning frameworks such as TensorFlow, Keras, PyTorch, and scikit-learn. Neha has successfully led projects on data integration and migration, and has hands-on experience with big data technologies like Hadoop and Spark. She holds a Bachelor's degree in Information Technology from the University of Mumbai and is certified in AWS Certified Data Analytics - Specialty. Neha's commitment to ensuring data quality and availability to support data-driven decision-making has made her a valuable asset. She is located in Jaipur and can be contacted at neha.gupta@example.com.",
        "location": "Jaipur",
        "email": "neha.gupta@example.com"
    }
]

# Generate a list of numbers from 1 to max_number
options = list(range(1, len(summaries_list) + 1))
if 'data' not in st.session_state:
    st.session_state.data = None
if 'emails_sent' not in st.session_state:
    st.session_state.emails_sent = []
# Create a dropdown with the generated list of numbers
batch_count = st.selectbox("Select a number:", options)
st.write(f"Selected batch count: {batch_count}")
# Example job description
job_description = """Job Description for Data Scientist Role
Position Title: Data Scientist

Location: Bangalore, India

Company Overview: Tech Innovators Pvt Ltd is at the forefront of technological advancement, pushing the boundaries of innovation. We are seeking a highly skilled and motivated Data Scientist to join our dynamic team. Our company specializes in providing cutting-edge solutions across various industries, leveraging big data and AI to drive impactful decisions.

Role Overview: The Data Scientist will play a pivotal role in designing and implementing advanced analytics models and algorithms to solve complex business problems. The individual will work closely with cross-functional teams, including data engineers, software developers, and business analysts, to deliver data-driven insights and solutions.

Key Responsibilities:

Analyze large, complex datasets to identify trends, patterns, and insights that can drive business decisions.

Develop and deploy machine learning models to optimize processes, forecast trends, and support decision-making.

Collaborate with stakeholders to understand business requirements and translate them into analytical solutions.

Perform data cleaning, preprocessing, and transformation to ensure data quality and integrity.

Visualize data and present findings in a clear and compelling manner to both technical and non-technical audiences.

Stay updated with the latest advancements in data science and machine learning technologies and apply them as needed.

Mentor junior data scientists and provide guidance on best practices in data science methodologies.

Qualifications:

Master’s degree or higher in Computer Science, Statistics, Mathematics, or a related field.

Proven experience (3+ years) as a Data Scientist or in a similar role, with a strong portfolio showcasing past projects.

Proficiency in programming languages such as Python, R, and SQL.

Hands-on experience with machine learning frameworks such as TensorFlow, Keras, PyTorch, and scikit-learn.

Expertise in data visualization tools like Tableau, Power BI, or Plotly.

Strong analytical, problem-solving, and communication skills.

Ability to work in a fast-paced environment and manage multiple projects simultaneously.

Knowledge of big data technologies like Hadoop, Spark, and cloud platforms (AWS, Azure, or Google Cloud).

Preferred Skills:

Experience with natural language processing (NLP) and deep learning.

Familiarity with version control systems such as Git.

Exposure to statistical software like SAS or SPSS.

Understanding of data privacy and security regulations.

Why Join Us?

Be part of a visionary company that is shaping the future of technology.

Work on challenging projects that make a real impact.

Collaborate with a diverse team of talented professionals.

Enjoy a competitive salary and comprehensive benefits package.

Access to continuous learning and development opportunities.

If you are passionate about data science and eager to make a difference, we invite you to apply and be a part of our innovative journey. To apply, please send your resume and a cover letter to careers@techinnovators.com."""
# Check if batch_count is selected before proceeding
if st.button("Send Invite"):
    with st.spinner('Processing data...'):
        st.session_state.data = interview_scheduler(summaries_list=summaries_list, batch_count=batch_count, job_description=job_description)
if st.session_state.data:
    for candidate in st.session_state.data:
        mailto_link = f"mailto:{candidate['candidate_email_id']}?subject={urllib.parse.quote(candidate['subject'])}&body={urllib.parse.quote(candidate['email_body'])}"
        if st.button(f"Send Email to {candidate['candidate_email_id']}"):
            webbrowser.open(mailto_link)
            st.session_state.emails_sent.append(candidate['candidate_email_id'])
    # Check if all emails have been sent
    if len(st.session_state.emails_sent) == len(st.session_state.data):
        st.success("All emails have been sent successfully!")