<h1 align="center">🧠 Sistema de Inferência com Machine Learning</h1>

<h2 align="center"> <i>Previsões Inteligentes para Precificação de Reservas de Hotéis com SageMaker e AWS</i></h2>

![Imagem|Compass](assets/compass.png)

## 📋 Índice

- [Objetivo](#-objetivo)
- [Descrição](#-descrição)
- [Como rodar](#-como-rodar)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Tecnologias utilizadas](#-tecnologias-utilizadas)
- [Arquitetura do projeto](#️-arquitetura-do-projeto)
- [Dificuldades](#️-dificuldades)
- [Agradecimentos](#-agradecimentos)
- [Autores](#-autores)

## 🎯 Objetivo
Construir um sistema de inferência para classificar reservas de hotéis com base em faixas de preços do [dataset do kaggle](https://www.kaggle.com/datasets/ahsan81/hotel-reservations-classification-dataset/).

## 📖 Descrição
1. Construção do Modelo de Classificação (Treinamento Local):
    - Realizamos o treinamento dos modelos de machine learning localmente, evitando gastos na AWS durante a fase de experimentação e ajuste de hiperparâmetros.
    - Avaliamos vários modelos, incluindo KNN, Decision Tree, Random Forest e XGBoost.
    - Escolhemos o XGBoost como o modelo final devido à sua melhor performance.

2. Armazenamento do Modelo Treinado no S3:
    - Após o treinamento, armazenamos o modelo XGBoost no Amazon S3 para posterior uso.

3. Criação do Ambiente Docker na AWS:
    - Criamos um ambiente Docker na Amazon Web Services (AWS) para implementar nossa API.

4. Desenvolvimento da API de Inferência:
    - Desenvolvemos um serviço em Python, utilizando o framework HTTP FastAPI.
    - A API carregou o modelo XGBoost treinado do Amazon S3 e expôs um endpoint para realizar inferências.
    - O endpoint aceita requisições POST com a rota /api/v1/predict e recebe um JSON no corpo da requisição contendo informações como o número de adultos, o número de crianças e o tipo de plano de refeições.
    - A resposta da API segue o formato: {"result": 1}.

5. Deploy do Serviço na AWS: 
    - Realizamos o deploy da API na AWS para que possa ser acessada remotamente.


## 🚀 Como rodar

1. Pré-requisitos

    - Docker
    - Python
 
2. Clone o repositório:

    ```bash
    git clone -b grupo-7 https://github.com/Compass-pb-aws-2024-ABRIL/sprints-4-5-pb-aws-abril.git
    cd sprints-4-5-pb-aws-abril
    ```
 
3. Para rodar:
    - Docker:
    

    Navegue para a pasta onde está localizado o Dockerfile.
    Construa a imagem Docker:
    
    ```bash
    docker build -t fastapi-docker .
    ```
    
    Rode o contêiner:
    
    ```bash
    docker run -p 80:80 fastapi-docker
    ```
    
    - Ou utilize os scripts .sh como helpers.

4. Acesse no navegador:

    Depois de montado, faça o download do seu modelo que está no S3 e é possível verificar a inferência via Postman. O endpoint é um método POST na rota localhost/api/v1/predict que deve receber um JSON no corpo seguindo o seguinte formato:
    ```JSON
    {
        "no_of_adults": 2,
        "no_of_children": 0,
        "no_of_weekend_nights": 2,
        "no_of_week_nights": 3,
        "type_of_meal_plan": "Not Selected",
        "required_car_parking_space": 0,
        "room_type_reserved": "Room_Type 1",
        "lead_time": 5,
        "arrival_year": 2018,
        "arrival_month": 11,
        "arrival_date": 6,
        "market_segment_type": "Online",
        "repeated_guest": 0,
        "no_of_previous_cancellations": 0,
        "no_of_previous_bookings_not_canceled": 1,
        "no_of_special_requests": 1
    }
    ```
    A resposta estará no seguinte formato:
    ```JSON
    {
        "result": 3
    }
    ```
    Sendo: 
    `result: 1` para preços ≤ 85; 
    `result: 2` para preços entre 80 e 115; 
    `result: 3` para preços >= 115.


5. ML & AI:
    - Navegue para a pasta Python e instale as bibliotecas necessárias.

    <br>
    
    ```bash
    pip install -r requirements.txt
    ```
    
    - Ou rode o arquivo setup.ipynb.
    Ajuste suas credenciais de acordo com o .env.example.

## 📂 Estrutura do Projeto

 
```bash
assets/                                 # imagens utilizadas no Readme
src/
├─ api/
├─├─ docker/                            # configurações Dockerfile
├─├─ docker-compose.yml                 # configurações docker-compose
├─├─ main.py                            # configuração FastAPI
├─├─ requirements.txt                   # dependências Python para a API
├─ python/
├─├─ data/                              # arquivos .csv antes e depois do processamento
├─├─ logs/                              # logs de cada modelo registrados durante o tuning
├─├─ models/                            # modelos iniciais/tuning do DT, KNN, RF e XGBoost
├─├─ sagemaker/
├─├─├─ eda.ipynb                        # analise dos dados e algumas manipulações das tabelas
├─├─├─ random_forest.ipynb              # treinamento com 2° melhor acurácia compatível com o SageMaker
├─├─├─ rds.ipynb                        # armazenamento do dataset original e alterado no AWS RDS
├─├─├─ train_script.py                  # script necessário para fazer o treinamento RF com SageMaker
├─├─├─ xgboost.ipynb                    # treinamento com melhor acurácia compatível com o SageMaker
├─├─ scripts/                           # funções utilizadas recorrentemente durante os treinamentos
├─├─ .env.example                       # armazenar variáveis do ambiente
├─├─ requirements.txt                   # dependências Python para AI & ML
├─├─ setup.ipynb                        # instalação das bibliotecas que serão utilizadas
README.md
```


## 💻 Tecnologias utilizadas

1. Tecnologias de Machine Learning e Bibliotecas de Python:
    - XGBoost: Algoritmo de aprendizado de máquina utilizado para a classificação.
    - Scikit-Learn: Utilizado para processamento dos dados, avaliação e modelos como KNN, Random Forest e Decision Tree.
    - Python: Linguagem de programação principal do projeto.


2. Ferramentas e Tecnologias para Desenvolvimento e Deploy:

    - AWS S3: Armazenamento do modelo treinado.
    - AWS EC2: Para a execução do ambiente Docker e hospedagem da API.
    - AWS RDS: Banco de dados MySQL.
    - AWS CLI: Interface de comando para o provisionamento da EC2.
    - Docker: Criação de um ambiente containerizado para a implementação da API.
    - FastAPI: Framework web em Python utilizado para o desenvolvimento da API de inferência.
    - Boto3: AWS SDK para o Python.


3. Controle de Versão e Colaboração:
    - Git: Controle de versão do código-fonte do projeto.
    - Trello: Organização e distribuição de tarefas.

4. Outros:
    - JSON: Formato de dados utilizado nas requisições e respostas da API.

## 🏗️ Arquitetura do projeto
![Imagem|Diagrama](assets/arquitetura.png)

## 🛠️ Dificuldades
1. <strong>Compreensão e Implementação de Modelos de Machine Learning</strong>:
Ajustar os hiperparâmetros para otimizar a performance exigiu um esforço significativo, com várias iterações e experimentos necessários para alcançar resultados satisfatórios.

2. <strong> Conexão do RDS com o banco de dados : </strong> A maior parte dos integrantes do grupo obteve problemas ao tentar realizar esta conexão.

3. <strong>Execução AWS SageMaker com LocalSession( )</strong>:
     Configurar e executar nossos scripts de machine learning no AWS SageMaker utilizando o LocalSession( ) apresentou dificuldades técnicas e não foi possível ser realizada até dia 20, um dia após a disponibilização deste [link](https://github.com/aws-samples/amazon-sagemaker-local-mode/blob/main/WINDOWS_INSTALLATION.md) no canal de tira-dúvidas. Depois foi possível rodar o LocalSession( ) utilizando WSL. Porém, como o tempo estava apertado não foi possível implementar completamente para utilizar no projeto.


## 🙏 Agradecimentos

É com imensa satisfação que o grupo-7 agradece à CompassUOL por providenciar o acesso aos cursos da Udemy, que geraram o aprendizado e desenvolvimento necessário para esta implementação e muito mais.

## 👥 Autores

**Pâmela Aliny Cleto Pavan**
- GitHub: https://github.com/PamelaPavan
