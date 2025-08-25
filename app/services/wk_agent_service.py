# Import namespaces
from importlib.resources import contents
import os
import asyncio
from dotenv import load_dotenv
from typing import Annotated
import json
import aiosqlite

from typing_extensions import TypedDict

from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain_openai import AzureChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.checkpoint.memory import InMemorySaver

class AgentService:

    class State(TypedDict):
        # Messages have the type "list". The `add_messages` function
        # in the annotation defines how this state key should be updated
        # (in this case, it appends messages to the list, rather than overwriting them)
        messages: Annotated[list, add_messages]

    def __init__(self):
        """
        Initializes the orchestrator with a storage service.

        :param storage_service: An instance of the storage service to interact with.
        """

        load_dotenv()  # Loads variables from .env into environment
        self.api_key = os.environ.get("AZURE_KEY")
        if self.api_key is None:
            raise ValueError("AZURE_KEY environment variable is not set.")

        project_name = os.environ.get("AZURE_ENDPOINT_NAME")

        self.endpoint = "https://foundy7za5.cognitiveservices.azure.com/"
        self.model_name = "gpt-4o"
        self.deployment_name = "gpt-4o"
        self.api_version = "2024-12-01-preview"

        os.environ["AZURE_OPENAI_API_KEY"] = self.api_key
        os.environ["AZURE_OPENAI_ENDPOINT"] = self.endpoint


    async def chat_agent(self, text: str) -> str:

        print("Initializing LangGraph...")

        graph_builder = StateGraph(AgentService.State)
        async with AsyncSqliteSaver.from_conn_string("data/checkpoints.db") as memory:


            llm = AzureChatOpenAI(
                azure_deployment=self.deployment_name,
                api_version=self.api_version,
                azure_endpoint=self.endpoint,
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2,
                # other params...
            )

            print("LLM initialized. {}", self.deployment_name)
            
            tool = TavilySearch(max_results=2)
            tools = [tool]

            # Modification: tell the LLM which tools it can call
            llm_with_tools = llm.bind_tools(tools)

            print("LLM with tools initialized.")

            def chatbot(state: AgentService.State):
                return {"messages": [llm_with_tools.invoke(state["messages"])]}  

            # The first argument is the unique node name
            # The second argument is the function or object that will be called whenever
            # the node is used.
            graph_builder.add_node("chatbot", chatbot)

            tool_node = ToolNode(tools=[tool])
            graph_builder.add_node("tools", tool_node)

            # The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
            # it is fine directly responding. This conditional routing defines the main agent loop.    
            graph_builder.add_conditional_edges(
                "chatbot",
                tools_condition,  # Routes to "tools" or "__end__"
                {"tools": "tools", "__end__": "__end__"}
            )

            # Any time a tool is called, we return to the chatbot to decide the next step
            graph_builder.add_edge("tools", "chatbot")

            graph_builder.add_edge(START, "chatbot")

            graph = graph_builder.compile(checkpointer=memory)

            print("LangGraph initialized. Ready to chat!")
            
            from langchain_core.runnables.config import RunnableConfig
            config: RunnableConfig = {"configurable": {"thread_id": "2"}}
            response = ""
            # infos: https://langchain-ai.lang.chat/langgraph/how-tos/streaming/#stream-multiple-modes
            async for event in graph.astream_events({"messages": [{"role": "user", "content": text}]}, config,  version="v1"):
                if event["event"] == "on_chat_model_stream":
                    data = event.get("data", {})
                    chunk = data.get("chunk")
                    if chunk and hasattr(chunk, 'content') and chunk.content:
                        response += chunk.content
                        print(chunk.content, end="", flush=True)
            
            print()  # Add newline at the end

        return response               
    

    async def chat_agent_memory(self, text: str) -> str:

        print("Initializing LangGraph...")

        graph_builder = StateGraph(AgentService.State)
        memory = InMemorySaver()

        llm = AzureChatOpenAI(
            azure_deployment=self.deployment_name,
            api_version=self.api_version,
            azure_endpoint=self.endpoint,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            # other params...
        )

        print("LLM initialized. {}", self.deployment_name)
        
        tool = TavilySearch(max_results=2)
        tools = [tool]

        # Modification: tell the LLM which tools it can call
        llm_with_tools = llm.bind_tools(tools)

        print("LLM with tools initialized.")

        def chatbot(state: AgentService.State):
            return {"messages": [llm_with_tools.invoke(state["messages"])]}  

        # The first argument is the unique node name
        # The second argument is the function or object that will be called whenever
        # the node is used.
        graph_builder.add_node("chatbot", chatbot)

        tool_node = ToolNode(tools=[tool])
        graph_builder.add_node("tools", tool_node)

        # The `tools_condition` function returns "tools" if the chatbot asks to use a tool, and "END" if
        # it is fine directly responding. This conditional routing defines the main agent loop.    
        graph_builder.add_conditional_edges(
            "chatbot",
            tools_condition,  # Routes to "tools" or "__end__"
            {"tools": "tools", "__end__": "__end__"}
        )

        # Any time a tool is called, we return to the chatbot to decide the next step
        graph_builder.add_edge("tools", "chatbot")

        graph_builder.add_edge(START, "chatbot")

        graph = graph_builder.compile(checkpointer=memory)

        print("LangGraph initialized. Ready to chat!")
        
        from langchain_core.runnables.config import RunnableConfig
        config: RunnableConfig = {"configurable": {"thread_id": "2"}}
        response = ""
        # infos: https://langchain-ai.lang.chat/langgraph/how-tos/streaming/#stream-multiple-modes
        for event in graph.stream({"messages": [{"role": "user", "content": text}]}, config):
            for value in event.values():
                print("Assistant:", value["messages"][-1].content)
                response = f"Assistant: {value['messages'][-1].content}"

        return response               