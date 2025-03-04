from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BaseAgent:
    """Base agent configuration for all specialized agents"""
    
    def __init__(self, model_name=None):
        self.model_name = model_name or os.getenv("DEFAULT_MODEL", "llama3-70b-8192")
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model_name=self.model_name
        )
        self.memory = ConversationBufferMemory(return_messages=True)
        
    def create_system_prompt(self, instructions):
        """Create a system prompt with the given instructions"""
        return SystemMessage(content=instructions)
    
    def create_human_message(self, content):
        """Create a human message with the given content"""
        return HumanMessage(content=content)
    
    def create_chat_prompt(self, system_instructions, human_template, input_variables=None):
        """Create a chat prompt template"""
        if input_variables is None:
            input_variables = []
            
        system_message = SystemMessage(content=system_instructions)
        human_message_template = HumanMessage(content=human_template)
        
        return ChatPromptTemplate.from_messages([system_message, human_message_template])
    
    def run_with_memory(self, prompt, input_dict=None):
        """Run the agent with memory"""
        if input_dict is None:
            input_dict = {}
            
        # Get chat history from memory
        chat_history = self.memory.chat_memory.messages
        
        # Combine history with new messages
        messages = chat_history + [prompt.format_messages(**input_dict)[0]]
        
        # Run the model
        response = self.llm.invoke(messages)
        
        # Update memory
        self.memory.chat_memory.add_message(response)
        
        return response