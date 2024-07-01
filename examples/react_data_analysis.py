"""A data analysis example implemented by assistant"""
import os
from pprint import pprint
from typing import Optional

# import qwen_agent.tools
from examples.agent.react_chat import ReActChat

# from qwen_agent.agents import ReActChat
from qwen_agent.gui import WebUI

ROOT_RESOURCE = os.path.join(os.path.dirname(__file__), 'resource')


def init_agent_service():
    llm_cfg = {
        # 'model': 'Qwen/Qwen1.5-72B-Chat',
        # 'model_server': 'https://api.together.xyz',
        # 'api_key': os.getenv('TOGETHER_API_KEY'),
        "model": "qwen-turbo",
        # "model": "qwen2-1.5b-instruct",
        "model_server": "dashscope",
        "api_key": "sk-cd8f0b15a37f47729f2dc7bba934c587",
    }
    tools = ['code_interpreter']
    bot = ReActChat(
        llm=llm_cfg,
        name="code interpreter",
        description="This agent can run code to solve the problem",
        function_list=tools,
    )
    return bot


def test(
    # query: str = "先读取文件，然后帮我画一个折线图来显示股价的变化",
    # query: str = "以时间维度分析各个街道人口变化情况",
    query: str = "画一个折线图展示沌口街人口数变化",
    file: Optional[str] = os.path.join(ROOT_RESOURCE, "person.csv"),
):
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = []

    if not file:
        messages.append({'role': 'user', 'content': query})
    else:
        messages.append({'role': 'user', 'content': [{'text': query}, {'file': file}]})

    for response in bot.run(messages):
        # pprint(response, indent=2)
        yield f"data: {response}\n\n"


def app_tui():
    # Define the agent
    bot = init_agent_service()

    # Chat
    messages = []
    while True:
        # Query example: pd.head the file first and then help me draw a line chart to show the changes in stock prices
        query = input('user question: ')
        # File example: resource/stock_prices.csv
        file = input('file url (press enter if no file): ').strip()
        if not query:
            print('user question cannot be empty！')
            continue
        if not file:
            messages.append({'role': 'user', 'content': query})
        else:
            messages.append({'role': 'user', 'content': [{'text': query}, {'file': file}]})

        response = []
        for response in bot.run(messages):
            print('bot response:', response)
        messages.extend(response)


def app_gui():
    bot = init_agent_service()
    chatbot_config = {
        'prompt.suggestions': [{
            'text': 'pd.head the file first and then help me draw a line chart to show the changes in stock prices',
            'files': [os.path.join(ROOT_RESOURCE, 'stock_prices.csv')]
        }, 'Draw a line graph y=x^2']
    }
    WebUI(bot, chatbot_config=chatbot_config).run()


if __name__ == '__main__':
    test()
    # app_tui()
    # app_gui()
