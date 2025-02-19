from datetime import datetime
from crewai import Agent, Task, Crew, Process, LLM
import os
import pytz
import json
crewai_agent = Agent(
    role="Candidate Selection Agent",
    goal="Select top candidates based on the given summaries, job descriptions, and batch numbers. Then, choose the best slots for candidates based on their locations and send emails for them to choose a preferred slot.",
    backstory="Specializing in candidate selection, this agent uses AI to evaluate candidate summaries against job descriptions, prioritize candidates by batch number, and organize interview slots based on candidate locations. The agent ensures that the top candidates are identified and that convenient interview times are suggested.",
    verbose=True,
    allow_delegation=True
)

os.environ["WATSONX_URL"]="https://us-south.ml.cloud.ibm.com"
os.environ["WATSONX_APIKEY"]="<API Key>"
os.environ["WATSONX_PROJECT_ID"]="<Project ID>"
llm = LLM(
    model="watsonx/mistralai/mistral-large",
    api_key="<API Key>"
)
candidate_selection_task = Task(
    description=(
        "Evaluate candidate summaries based on the given job descriptions (JD) and batch numbers. "
        "Identify the top candidates for each batch and arrange interview slots based on the candidates' locations. "
        "Then, prepare emails for the candidates with 2 to 3 available slots for them to choose from. "
        "The provided summaries include candidate details like email IDs and locations."
        " "
        "Inputs: "
        "1. Summaries list: {summaries_list} - Each element is a dictionary with summary of one candidate, including email ID and location, all as different keys in dictionary."
        "2. Batch count: {batch_count} - A number representing the number of total candidates needs to be selected from the given summary list. The selected profile needs to be equal to this number only, not less not more. If we have the same number of profiles in the summary list as the batch count, select all, and draft mail accordingly as per the instruction."
        "3. Job description (JD): {job_description} - A string input describing the job requirements."
        "4. Current date and time in GMT: {current_datetime} - Current timestamp in GMT."
        " "
        "Steps: "
        "1. Parse the candidate summaries and extract email IDs, locations, and other relevant information. "
        "2. Match the candidate skills and experiences with the job descriptions (JD). "
        "3. Rank the candidates based on the match quality and batch numbers. "
        "4. Select the top {batch_count} candidates, ensuring the number of candidates selected matches the batch count. "
        "5. Determine suitable interview slots based on the candidates' locations and current date and time in GMT. Time slots given to candidates should be based on their timezone, which we need to identify from their location, and provide slots in their respective timezone rather than GMT. "
        "6. Prepare personalized emails to the candidates with 2 to 3 slot options for them to choose from, incorporating details from the JD. Ensure the email body is formatted as a plain text string for direct use in emails. "
        "7. Return a list of dictionaries containing the email_body (as plain text), subject, and candidate_email_id for each candidate."
    ),
    expected_output=(
        "Return a JSON list string representing a list of JSON elements, each containing the email body (as plain text), subject, and candidate email ID for the top candidates. "
        "Do not send truncated response at all, need valid JSON list string representing a list of JSON elements. "
        "Selected candidate number should be strictly equal to batch_count only not more or less. "
        "The email body should include 2 to 3 interview slot options for the candidates to choose from and should be personalized based on the job description."
    ),
    agent=crewai_agent
)

def interview_scheduler(summaries_list, batch_count, job_description):
    crew = Crew(agents=[crewai_agent], tasks=[candidate_selection_task], manager_llm=llm, process=Process.hierarchical, verbose=True)
    current_datetime = datetime.now(pytz.timezone("GMT"))
    document_inputs = {
        'summaries_list': summaries_list,
        'batch_count': batch_count,
        'job_description': job_description,
        'current_datetime': str(current_datetime),
    }
    out = crew.kickoff(inputs=document_inputs)
    try:
        if 'json' in out.raw.lower():
            out = json.loads(out.raw.replace('```json\n', '').replace('```', '').replace('"""', '"').replace('\n', ''))
        elif 'python' in out.raw.lower():
            out = json.loads(out.raw.replace('```python\n', '').replace('```', '').replace('"""', '"').replace('\n', ''))
        else:
            out = json.loads(out.raw.replace('```', '').replace('```', '').replace('"""', '"').replace('\n', ''))
    except:
       out = interview_scheduler(summaries_list=summaries_list, batch_count=batch_count, job_description=job_description)
    return out
