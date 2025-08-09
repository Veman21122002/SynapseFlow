from langchain_huggingface import HuggingFaceEndpoint,ChatHuggingFace
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv
from langgraph.graph import START,END,StateGraph
from langchain_core.messages import SystemMessage,HumanMessage,BaseMessage
from typing import TypedDict,Annotated,Literal
from langgraph.graph.message import add_messages

load_dotenv()
#state
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage],add_messages] 


model = HuggingFaceEndpoint(
    repo_id='openai/gpt-oss-120b',
    task='conversational'
)

llm = ChatHuggingFace(llm = model)

def chat_node(state:ChatState):
    #take user query from state
    messages = state['messages']
    # send the query to llm
    response = llm.invoke(messages)
    # store response  in state
    return {'messages':[response]}

checkpointer = MemorySaver()
graph= StateGraph(ChatState)

graph.add_node('chat_node',chat_node)

graph.add_edge(START,'chat_node')
graph.add_edge('chat_node',END)

workflow = graph.compile(checkpointer=checkpointer)

