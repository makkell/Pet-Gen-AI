import langchain_helper as lch
import streamlit as st
import hg_helper as hg

@st.cache_data(show_spinner=False)
def get_pet_names(animal_type, pet_color):
    return lch.generate_pet_name(animal_type, pet_color)

@st.cache_data(show_spinner=False)
def get_promt(pet, pet_name, pet_color):
     return lch.generate_prompt_for_hg(pet, pet_name, pet_color)

@st.cache_data(show_spinner=False)
def get_image_pet(promt):
     return hg.generate_pet_of_prompt(promt)

st.title('Питомец')

animal_type = st.sidebar.selectbox("Какой ваш любимый питомец?", ('Кот', 'Собака', 'Попугай'))


if animal_type in ('Собака', 'Кот', 'Попугай'):
    pet_color = st.sidebar.text_area(
          label="Какой цвет питомца?", 
          max_chars=25
        )
    
response = None

if pet_color:
    if response is None:
        response = get_pet_names(
            animal_type=animal_type,
            pet_color=pet_color
            )
        st.text(response)

    if response:
        pet_names = response.split()[1::2]
        pet_name = st.selectbox("Выберите одно предложенное имя:", pet_names)

        if st.button("Подтвердить выбор"):
            st.success(f"Генерируется изображение вашего питомца: {pet_name}")
            promt = get_promt(animal_type, pet_name, pet_color)
            image = get_image_pet(promt)
            if image:
                st.image('pet_image.png')
        
