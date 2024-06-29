from fastapi import FastAPI, Request
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent, AgentType
from langchain.tools import AIPluginTool
from fastapi.middleware.cors import CORSMiddleware
import os

# Setup environment variables
URL = os.environ['API_URL']

# Initialize LLM
llm = ChatOpenAI(temperature=0)

# AI Agent initialization
tools = load_tools(["requests_post"], allow_dangerous_tools=True)
ai_tool = AIPluginTool.from_plugin_url(URL + "/.well-known/ai-plugin.json")
tools += [ai_tool]

agent_chain = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True
)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Question(BaseModel):
    question: str


@app.post("/ask")
async def ask_question(request: Request, question: Question):
    result = agent_chain.run(question.question)
    return {"result": result}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
