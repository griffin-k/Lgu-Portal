import datetime
from langchain_google_genai import GoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAI, HarmBlockThreshold, HarmCategory
from langchain.tools import Tool
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate

api_key = "AIzaSyAVremZ8j3CWnUxBwZ8jZQUpaY16EB68cY"
llm = GoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=api_key,
    safety_settings={
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    },
)


def get_time(_):
        now = datetime.datetime.now()
        formatted_time = now.strftime("%H:%M:%S")
        return f"The current system time is: {formatted_time }"

def get_battery(_):
        return f"88%"


time_tool = Tool(
        name="Time Tool",
        description="Return time current time from the system this is the time for pakistan.",
        func=get_time
)
battery_tool = Tool(
        name="Battery Tool",
        description="Return the current battery percentage of the laptop",
        func=get_battery
)
tools = [time_tool, battery_tool]


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
output = agent_executor.invoke({"input": "where is pakistan. what the current time is"})

print(output["output"])