import requests
import telegram
from telegram.ext import CommandHandler, Updater

# Função para lidar com o comando /cpf
def cpf_handler(update, context):
    # Dados de autenticação
    headers = {
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://si-pni.saude.gov.br/',
        'sec-ch-ua-mobile': '?0',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43',
        'sec-ch-ua-platform': '"Windows"',
    }

    # Obter CPF do usuário
    cpf = update.message.text.split()[1]
    
    # Fazer a requisição para obter os dados do CPF
    response = requests.get(f'https://servicos-cloud.saude.gov.br/pni-bff/v1/cidadao/cpf/{cpf}', headers=headers)
    data = response.json()

    # Verificar se a resposta foi bem-sucedida
    if response.status_code == 200:
        try:
            record = data['records'][0]

            # Extrair os dados do registro
            cns_definitivo = record['cnsDefinitivo']
            nome = record['nome']
            cpf = record['cpf']
            data_nascimento = record['dataNascimento']
            sexo = record['sexo']
            nome_mae = record['nomeMae']
            ativo = record['ativo']
            obito = record['obito']
            telefone = record['telefone'][0]
            ddd = telefone['ddd']
            numero_telefone = telefone['numero']
            numero_endereco = record['endereco']['numero']
            cep = record['endereco']['cep']

            # Enviar os dados para o usuário
            message = f"CNS Definitivo: {cns_definitivo}\n"
            message += f"Nome: {nome}\n"
            message += f"CPF: {cpf}\n"
            message += f"Data de Nascimento: {data_nascimento}\n"
            message += f"Sexo: {sexo}\n"
            message += f"Nome da Mãe: {nome_mae}\n"
            message += f"Ativo: {'Sim' if ativo else 'Não'}\n"
            message += f"Óbito: {'Sim' if obito else 'Não'}\n"
            message += f"Telefone: ({ddd}) {numero_telefone}\n"
            message += f"Número do Endereço: {numero_endereco}\n"
            message += f"CEP: {cep}"

            update.message.reply_text(message)
        except IndexError:
            update.message.reply_text("CPF não encontrado")
    else:
        update.message.reply_text("Erro ao consultar CPF")

# Criar instância do bot do Telegram
bot_token = '6177077604:AAEoBC-JNywDBVT9cHZQwDSYk3gaCLRzSKU'
updater = Updater(token=bot_token, use_context=True)
dispatcher = updater.dispatcher

# Criar tratador de comandos para o comando /cpf
cpf_handler = CommandHandler('cpf', cpf_handler)
dispatcher.add_handler(cpf_handler)

# Iniciar o bot
updater.start_polling()