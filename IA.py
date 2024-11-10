import os
from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader, PyPDFLoader
from key import API_KEY
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from PyPDF2 import PdfReader

# Configurar variáveis de ambiente
os.environ['GROQ_API_KEY'] = API_KEY
os.environ['USER_AGENT'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'

def carrega_site_web():
    # Carregar documentos da web
    url_site = input('Digite a URL do site: ')
    loader = WebBaseLoader(url_site)
    lista_de_documento = loader.load()
    documento = ''
    for doc in lista_de_documento:
        documento += doc.page_content
    return documento

def carrega_pdf():
    # Carregar documentos do PDF
    pdf_path = input('Digite o caminho do arquivo PDF: ')
    loader = PyPDFLoader(pdf_path)
    lista_documentos = loader.load()
    documento = ''
    for doc in lista_documentos:
        documento += doc.page_content
    return documento

def carrega_youtube():
    # Carregar transcrição do YouTube
    youtube_url = input('Digite a URL do vídeo do YouTube: ')
    loader = YoutubeLoader.from_youtube_url(youtube_url, language=['pt'])
    lista_documentos = loader.load()
    documento = ''
    for doc in lista_documentos:
        documento += doc.page_content
    return documento

# Selecionar o modelo de linguagem
chat = ChatGroq(model='mixtral-8x7b-32768')

def mensagem_bot(mensagens, documento):
    # Limitar o tamanho do documento
    max_length = 15000
    documento = documento[:max_length]
    
    # Criar mensagens modelo
    mensagens_modelo = [
        ('system', f'Você é um modelo amigável, que fala português, com ampla experiência em marketing, programação, cálculo, álgebra linear e economia. Você se chama Dr. Big Wall e tem acesso aos seguintes documentos para dar suas respostas caso precisar: {documento}')
    ]
    mensagens_modelo += mensagens
    
    # Criar o template de chat e gerar a resposta
    template = ChatPromptTemplate.from_messages(mensagens_modelo)
    chain = template | chat
    return chain.invoke({}).content

def main():
    print('Bem-vindo ao Sattobot')
    texto_selecao = '''Digite 1 se você quiser conversar com um site da web
Digite 2 se você quiser conversar com um vídeo do YouTube
Digite 3 se você quiser conversar com um PDF
Digite x para sair
'''
    mensagens = []
    documento = ''
    
    while True:
        selecao = input(texto_selecao)
        if selecao == '1':
            documento = carrega_site_web()
            break
        elif selecao == '2':
            documento = carrega_youtube()
            break
        elif selecao == '3':
            documento = carrega_pdf()
            break
        elif selecao.lower() == 'x':
            return
        else:
            print('Seleção inválida. Tente novamente.')
    
    while True:
        pergunta = input('Usuário: ')
        if pergunta.lower() == 'x':
            break
        mensagens.append(('user', pergunta))
        resposta = mensagem_bot(mensagens, documento)
        mensagens.append(('assistant', resposta))
        print(f'Bot: {resposta}')
    
    # Exibir o histórico de mensagens após sair do loop
    print('\nHistórico de Mensagens:')
    for role, content in mensagens:
        print(f'{role.capitalize()}: {content}')

if __name__ == "__main__":
    main()