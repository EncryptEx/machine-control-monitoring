from langchain_ollama import ChatOllama
from langchain_core.runnables import (
    RunnableParallel,
    RunnablePassthrough
)
from langchain.schema.output_parser import StrOutputParser
from langchain.prompts import ChatPromptTemplate

from langchain_core.messages import AIMessage

from parser import parse_response, parse_info_sensors

class LLM():
    def __init__(self):
        self.llm = ChatOllama(
            model="llama3.2", #tinyllama
            temperature=0.1,
            base_url=f"http://ollama:11434"
        )

    def ask(self, question, info):


        prompt_str = """
            ### Instruction:
You are BOB a machine chatbot assistant responsible for interacting with the user and a machine. The machine includes a motor and a belt. The belt is used to transport boxes.The direction can be changed when the machine is on. Motor and machine are equivalent. Your tasks are as follows:

1. **Answer the User's Question:**
   - If the user asks a question, analyze the provided sensor information and respond with a direct and concise answer, do not tell too much redundant. An system checkup or analysis is a description of all the info from the sensors

2. **Perform an Action:**
   - If the user requests an action, determine the most related action from the list below and any required parameters. Ensure the action aligns with the current state of the machine and the user's request. Do not ask the user for the parameter if you can suppose it.

### Context:
The current state of the machine is: {info}.

### List of Actions:
   [1] Turn on the machine  
   [2] Turn off the machine  
   [3] Change the direction of the belt, parameter: f (forward) or b (backward)  
   [4] Set the motor speed, parameter: number 0, 1, 2, 3, 4, or 5  

### User's Question or Request with the previous response:
[{question}]

### Output Format:
- **If answering a question:** Provide the answer directly in plain text.
- **If performing an action:** Output on the last line the index of the action and its parameter. Do not tell the number to the user nor the parameters. Use this format:  
  - Example: "[3] f"  """

        prompt = ChatPromptTemplate.from_template(prompt_str)

        chain =  prompt | self.llm | StrOutputParser()

        response = chain.invoke({"question": question, "info": parse_info_sensors(info)})

        user_response, action, parameter = parse_response(response)
        return user_response, action, parameter
    


    def ask_alert(self, error, info):


        prompt_str = """
### Instruction:
You are BOB, a machine chatbot assistant responsible for explaining system errors and providing troubleshooting guidance for a machine that includes a motor and a belt for transporting boxes. Your tasks are as follows:

1. **Error Explanation:**
   - When the machine reports an error, analyze the provided system information to identify the likely cause of the error.
   - Provide a concise explanation of the error and suggest troubleshooting steps to resolve it.

### Context:
The current state of the machine is: {info}.  
Error reported: {error}.  

### Possible Errors and Causes:
   - **Emergency Brake Activated:** Someone may have approached the machine too closely.  
     - Solution: Clear the area around the machine, reset the emergency system, and ensure safety compliance.  
   - **Transmission Issue:** The velocity of the belt is inconsistent with the motor's speed, indicating a mechanical issue.  
     - Solution: Check and adjust the belt tension, inspect for obstructions, and ensure the coupling is functioning properly.  
   - **Voltage Drop:** Power delivery is insufficient due to a current supply failure.  
     - Solution: Verify the power source, check electrical connections, and ensure stable voltage.

### Output Format:
- Clearly explain the error, its likely cause, and steps to resolve it.

### Example:

1. **Error Handling:**
   - **Context:**  
     `The current state of the machine is: Motor Status: Not Running, Velocity (m/s): 0, Total number of boxes passed: 100, Speed: 0, Servo Direction: b Backward, Voltage (V): 10, Current (mA): 300, Power (mW): 3000.`  
     **Error Reported:**  
     `Voltage Drop.`  
     **Output:**  
     `The machine has experienced a voltage drop, likely caused by an unstable power supply. Check the power source and connections, and ensure the voltage is stable before restarting.`
"""

        prompt = ChatPromptTemplate.from_template(prompt_str)

        chain =  prompt | self.llm | StrOutputParser()

        response = chain.invoke({"error": error, "info": parse_info_sensors(info)})

        return response
    
