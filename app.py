import streamlit as st
import google.generativeai as genai
import settings
import dict_cars
import os
from PIL import Image

# Configure sua API key do Google Generative AI
API_KEY = 'AIzaSyCXfTt4VVgwcxq9nvAsIO7x5yNsn5BtDjE'  # Substitua pela sua API KEY
genai.configure(api_key=API_KEY)

# Carregue o dicionário de carros
cars = dict_cars.cars

def generate_response(conversation, message):
    """Gera uma resposta do chatbot usando o Google Gemini."""

    generation_config = {
        "temperature": 0.7,
        "top_p": 1,
        "top_k": 0,
        "max_output_tokens": 256,
    }
    model = genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config=generation_config,
        safety_settings=settings.safety_settings
    )

    conversation = [
    {"role": "system", "content": "Você é um chatbot que fornece informações sobre Ayrton Senna."},
    ] 
    exemplos_senna = [
    {
        "role": "user", 
        "content": "Em que ano Ayrton Senna começou na Fórmula 1?"
    },
    {
        "role": "assistant", 
        "content": "Ayrton Senna estreou na Fórmula 1 em 1984, pilotando para a equipe Toleman."
    },
    {
        "role": "user", 
        "content": "Quantos títulos mundiais Ayrton Senna ganhou?"
    },
    {
        "role": "assistant", 
        "content": "Ayrton Senna conquistou três campeonatos mundiais de Fórmula 1, em 1988, 1990 e 1991."
    },
    {
        "role": "user", 
        "content": "Qual era o carro de Senna em 1990?"
    },
    {
        "role": "assistant", 
        "content": "Em 1990, Ayrton Senna pilotou o McLaren MP4/5B, um carro icônico que o ajudou a conquistar seu segundo título mundial."
    },
    {
        "role": "user", 
        "content": "Me fale sobre a vitória de Senna em Mônaco em 1987."
    },
    {
        "role": "assistant", 
        "content": "A vitória de Senna em Mônaco em 1987 foi dominante. Pilotando o Lotus 99T, ele liderou a corrida de ponta a ponta, demonstrando grande habilidade em um circuito desafiador. Essa foi sua primeira vitória no famoso GP de Mônaco." 
    }
]
    conversation.append({"role": "user", "content": message})

    # Cria o prompt como uma string
    prompt = ''.join([f"{message['role']}: {message['content']}\n" for message in conversation])

    # Passa o prompt dentro de uma lista para 'contents'
    response = model.generate_content(
        contents=[prompt] 
    )

    conversation.append({"role": "assistant", "content": response.text}) # Acessa o texto da resposta
    return conversation, response.text # Retorna o texto da resposta


# Caminho para o diretório das imagens 
image_dir = '/home/matheus/repos_github/projetos_matheus/DesafioAlura2024/images'

def get_senna_info(year):
    """Retorna informações sobre Ayrton Senna, seu carro e a imagem 
       correspondente ao ano.
    """

    if year in cars:
        car_info = cars[year]
        model = car_info["model"]
        description = car_info["description"]
        titles = car_info["titles"]
        wins = car_info["wins"]
        
        # Monta o nome do arquivo de imagem
        image_file = f"{year}_{model}.jpg"
        image_path = os.path.join(dict_cars.image_dir, image_file)

        # Verifica se a imagem existe
        if os.path.isfile(image_path):
            image = Image.open(image_path)
            st.image(image, caption=f"{year} - {model}", use_column_width=True)
        else:
            st.write(f"Imagem para o {model} de {year} não encontrada.")

        return f"Em {year}, Ayrton Senna pilotou o {model}. {description} Ele conquistou {titles} título mundial e {wins} vitórias nesse ano."

    else:
        return "Informações sobre esse ano não estão disponíveis."

def main():
    st.set_page_config("Ayrton Senna: Uma Lenda", layout="wide")
    st.title("Ayrton Senna: Uma Lenda nas Pistas")

    # Lista os anos disponíveis
    available_years = list(cars.keys())
    available_years.sort()

    # Inicializa a conversa com uma mensagem de boas-vindas
    conversation = [
        {"role": "system", "content": "Você é um chatbot que fornece informações sobre Ayrton Senna."}
    ]

    # Barra lateral com informações sobre o chatbot
    with st.sidebar:
        #st.image("images/carro.png")  # Substitua pela imagem desejada
        st.markdown(
            """
            ## Bem vindo ao *Ayrton Senna: Uma Lenda*.
            ## Converse com nosso chatbot e conheça a trajetória do piloto brasileiro e seus carros.
            ------------------------------------------
            ## Como usar o chatbot:
            * Digite suas perguntas sobre Ayrton Senna na caixa de texto abaixo.
            * O chatbot fornecerá informações sobre a carreira de Senna, seus carros, vitórias e títulos.
            """
        )

    # Exibe o histórico da conversa
    for message in conversation:
        if message["role"] == "user":
            st.write("Você:", message["content"])
        else:
            st.write("Chatbot:", message["content"])

     # Obtém a entrada do usuário
    user_input = st.text_input("Digite sua pergunta:")
    if user_input:
        # Verifica se a pergunta é sobre um ano específico
        if user_input.lower().startswith("em que ano") or user_input.lower().startswith("qual era o carro"):
            try:
                year = int(user_input.split()[-1])  # Extrai o ano da pergunta
                response = get_senna_info(str(year))
            except ValueError:
                response = "Por favor, especifique o ano em sua pergunta."
        else:
            conversation, response = generate_response(conversation, user_input)

        # Exibe a resposta do chatbot, incluindo a imagem se disponível
        st.write("Chatbot:", response)

if __name__ == "__main__":
    main()