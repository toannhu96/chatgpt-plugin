from langchain.chat_models import ChatOpenAI
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType
from langchain.tools import AIPluginTool


if __name__ == '__main__':
    # Setup environment variables
    import os
    URL = os.environ['API_URL']

    llm = ChatOpenAI(temperature=0)

    # AI Agent does best when it only has one available tool
    # to engage with URLs
    tools = load_tools(["requests_post"], allow_dangerous_tools=True)

    # AIPluginTool only fetches and returns the openapi.yaml linked to in /.well-known/ai-plugin.json
    # This may need some more work to avoid blowing up LLM context window
    tool = AIPluginTool.from_plugin_url(URL + "/.well-known/ai-plugin.json")
    tools += [tool]

    # Setup an agent to answer the question without further human feedback
    agent_chain = initialize_agent(
        tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True, handle_parsing_errors=True)

    # Ask the question, and the agent loop
    # agent_chain.run(
    #     "How many lamports does ArTbfyWWNBLkDhU2ar8RBEPDHkEv6jVWJTwxjDnVYnMX have?")
    # agent_chain.run(
    #     "What happened in transaction 3WajPhgXqL2UdxpBDDigLokdBT1AnL1srN5fL9hGoejcNCVb2bYyGdEF31WspnP7wmNu5aW1Ab87ocKWZQnt29az ?")
    agent_chain.run(
        "What happened in transaction 5dY6LRgMFexKhVs5yzLefvfGpWkMT1ZZ9TBQPyrskndRqnZCs18SqroywXkLvUSbnWFFAhShKmQT3zh9pYVVUbei ?")
