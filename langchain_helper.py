import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI # инициализация модели 
from langchain_core.prompts import PromptTemplate # класс шаблона промта 
from langchain_core.output_parsers import StrOutputParser # парсер ответа модели

from langchain_community.agent_toolkits.load_tools import load_tools # инструменты для агента
from langchain.agents import initialize_agent # инициализация агента
from langchain.agents import AgentType #выбор типа агента


load_dotenv()


def generate_prompt_for_hg(pet, pet_name, pet_color):
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        model="qwen/qwen3-4b-2507",   # поставьте id модели из LM Studio
        temperature=0.7,
    )

    prompt_template = PromptTemplate(
        input_variables=['animal_type', 'pet_color'],
        template='Напиши промпт для генеративной модели black-forest. Нужно попросить ее нарисовать животное по следующим параметрам:' \
        'Животное : {pet}' \
        'Имя: {pet_name}' \
        'Цвет: {pet_color}' \
        'Важно чтобы цвет имел значение, чтобы питомец был преимущественно нужного цвета:{pet_color}' \
        'Если имя питомца говорящее, допустим "молния", то должна быть соотвествущая тематика.' \
        'Написать промт нужно на английском языке.'
    )

    chain = prompt_template | llm | StrOutputParser()

    response = chain.invoke({
        'pet': pet,
        'pet_name': pet_name,
        'pet_color': pet_color
    })

    return response

def generate_pet_name(animal_type, pet_color):
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        model="qwen/qwen3-4b-2507",   # поставьте id модели из LM Studio
        temperature=0.7,
    )
    prompt_template = PromptTemplate(
        input_variables=['animal_type', 'pet_color'],
        template='Напиши мне 5 интересных имен для моего домашнего питомца {animal_type}, цвет питомца {pet_color}. Кратко, только список.' \
        'Оформи список вида:' \
        '1. что-то' \
        '2. что-то' \
        '3. ....' \
        'Пиши все строго на русском.'
    )

    chain = prompt_template | llm |  StrOutputParser()

    response =  chain.invoke({
        'animal_type':animal_type,
        'pet_color' : pet_color
    })

    return response

#TODO сделать полноценного агента, используя поиск по вики описание породы питомца для лучшей генерации
def langchain_agent():
    llm = ChatOpenAI(
        base_url="http://localhost:1234/v1",
        model="qwen/qwen3-4b-2507",
        temperature=0.7
    )

    tools = load_tools(['wikipedia', 'llm-math'], llm=llm)

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent= AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=1
    )

    result = agent.invoke(
        "Ищи информацию в вики. Какой средний возраст собаки? Умножь число на 3."
    )
    print(result['output'])



if __name__ == "__main__":
    # langchain_agent()
    # print(generate_pet_name(animal_type='Кот', pet_color='Черный'))
    print(generate_prompt_for_hg('Кот', "Молния", "Черный"))