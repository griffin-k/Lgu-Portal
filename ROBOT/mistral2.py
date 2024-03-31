from transformers.tools import HfAgent
from transformers import Tool
import datetime
import psutil

class Toggle_Theme(Tool):
    name = "Theme_Toggle"
    description = "This tool allows you to switch between the system's light and dark theme modes as mentioned in the query. Pick either 'dark' or 'light'"
    inputs = ["text"]
    outputs = []

    def __call__(self, mode):
        query = f"Switched to {mode}"
        print(query)

class Get_System_Time(Tool):
    name = "Get_System_Time"
    description = "This tool retrieves the current system time."

    inputs = ["text"]
    outputs = ["text"]

    def __call__(self):
        now = datetime.datetime.now()
        formatted_time = now.strftime("%H:%M:%S")
        return f"The current system time is: {formatted_time}"

class Get_Battery_Percentage(Tool):
    name = "Get_Battery_Percentage"
    description = "This tool displays the current battery percentage of your system (if supported)."

    inputs = ["text"]
    outputs = ["text"]

    def __call__(self):
        try:
            battery = psutil.sensors_battery()
            if battery.percent is None:
                return "Battery information not available."
            percentage = battery.percent
            message = f"Battery Percentage: {percentage}%"
            return message
        except (AttributeError, ImportError):
            return "Error: 'psutil' library not installed or unsupported system."

# Initialize the agent with the model URL and additional tools
agent = HfAgent("https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1", additional_tools=[Toggle_Theme(), Get_System_Time(), Get_Battery_Percentage()])

# Chat with the agent
agent.chat("you know what the time now ")
