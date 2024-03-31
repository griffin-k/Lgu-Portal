import datetime
import re
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain.tools import Tool
from langchain_community.llms import HuggingFaceEndpoint
from langchain_community.llms import HuggingFaceTextGenInference
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage
import psutil
import requests







ENDPOINT_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HF_TOKEN = "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"


# llm=HuggingFaceEndpoint(
#     repo_id=ENDPOINT_URL, max_length=128, temperature=0.5,

#     server_kwargs={
#         "headers": {
#             "Authorization": f"Bearer {HF_TOKEN}",
#             "Content-Type": "application/json",
#         }
#     },
# )






llm = HuggingFaceTextGenInference(
    inference_server_url=ENDPOINT_URL,
    max_new_tokens=512,
    top_k=50,
    temperature=0.1,
    repetition_penalty=1.03,
    server_kwargs={
        "headers": {
            "Authorization": f"Bearer {HF_TOKEN}",
            "Content-Type": "application/json",
        }
    },
)






# api_key = "AIzaSyAVremZ8j3CWnUxBwZ8jZQUpaY16EB68cY"
# llm = GoogleGenerativeAI(
#     model="gemini-pro",
#     google_api_key=api_key,
#     safety_settings={
#         HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
#     },
# )



def time(_):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%I:%M %p")
    return formatted_time
 

def battery(_):
    battery_percentage = psutil.sensors_battery().percent
    return battery_percentage
    
    
def screen_time(_):
        uptime_seconds = psutil.boot_time()
        screen_time_seconds = psutil.time.time() - uptime_seconds
        screen_time_formatted = str(psutil.time.strftime('%H:%M:%S', psutil.time.gmtime(screen_time_seconds)))
        return screen_time_formatted
      
def weather(_):
    url = f'https://wttr.in/lahore?format=%t+%C+%w'
    response = requests.get(url)
    response.raise_for_status()  
    weather_info = response.text.strip().split()
    temperature = weather_info[0]
    condition = ' '.join(weather_info[1:-1])
    wind_speed = weather_info[-1]
    speed =re.sub(r'[/a-z]', '', wind_speed)
    return temperature
    












def chat(query):
    messages = [
    SystemMessage(
        content="You are a helpful AI that shares everything you know. Talk in English."
    ),
    HumanMessage(content=query),
]
 
    return llm.invoke(messages).content
     







weather_tool= Tool(
        name="weather Tool",
        description="This tool is used to get the current weather Status of lahore",
        func=weather
)

time_tool = Tool(
        name="Time Tool",
        description="Return time current time from the system this is the time for pakistan.",
        func=time
)
battery_tool = Tool(
        name="Battery Tool",
        description="Return the current battery percentage of the laptop",
        func=battery
)

screen_tool = Tool(
        name="Screen Tool",
        description="This tool get the scrreen time of a labtop",
        func=screen_time
)

general_questions_tool = Tool(
        name="Ask General Question",
        description="This tool answer to the queries which cannot be answered through tools ",
        func=chat
)

tools = [time_tool, battery_tool,screen_tool, general_questions_tool,weather_tool]


# Get the prompt to use - you can modify this!
# prompt = hub.pull("hwchase17/react")
template = """
Act as a helpful assistant that talks nicely to its users. only use tools when required otherwise answer it by yourself 
Answer the following questions as best you can. You have access to the following tools:
{tools}
Use the following format:
Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question
Begin!
Question: {input}
Thought:{agent_scratchpad}"""



prompt = PromptTemplate(
        template=template,
        input_variables=['agent_scratchpad', 'input', 'tool_names', 'tools']
)
agent = create_react_agent(llm, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,handle_parsing_errors=True)

while 1:
    prompt=input("You: ")
    output = agent_executor.invoke({"input": {prompt}})
    print(output["output"])