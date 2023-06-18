import requests
from telegram.ext import Updater, CommandHandler

def start(update, context):
    chat_id = update.effective_chat.id
    context.bot.send_message(chat_id=chat_id, text="Olá! Por favor, digite o CPF que deseja consultar.")

def consultar_cpf(update, context):
    cpf = update.message.text
    headers = {
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://si-pni.saude.gov.br/',
        'sec-ch-ua-mobile': '?0',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiIyOTkwOTY2Mjg1MCIsIm9yaWdlbSI6IlNDUEEiLCJpc3MiOiJzYXVkZS5nb3YuYnIiLCJub21lIjoiTElESUEgQU1FTElBIEZFTElYIERBIFNJTFZBIiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9TSS1QTklfT0VTQyIsIlJPTEVfU0lWRVBHUklQRS1OT1ZPX09QUk1VTiIsIlJPTEVfU0ktUE5JX0dNIiwiUk9MRV9TQ1BBU0lTVEVNQV9HRVMiLCJST0xFX1NJLVBOSSIsIlJPTEVfU0lWRVBHUklQRS1OT1ZPIiwiUk9MRV9TQ1BBX0dFUyIsIlJPTEVfU0NQQV9VU1IiLCJST0xFX1NDUEFTSVNURU1BIiwiUk
    9MRV9TQ1BBIl0sImNsaWVudF9pZCI6IlNJLVBOSSIsInNjb3BlIjpbIkNOU0RJR0lUQUwiLCJHT1ZCUiIsIlNDUEEiXSwiY25lcyI6Im51bGwiLCJvcmdhbml6YXRpb24iOiJEQVRBU1VTIiwiY3BmIjoiMjk5MDk2NjI4NTAiLCJleHAiOjE2ODcxMTcwOTUsImp0aSI6ImE4ZDMwNGMxLTExY2EtNGVkNS05MzNlLTI1MGMyZmFiZDMyOSIsImtleSI6IjI5NzAzIiwiZW1haWwiOiJsaWdhbGVvbmFAaG90bWFpbC5jb20ifQ._0xh59bU7IyQEiMlxtCoWfHHCGM5JMTf1dbYchrZXx8',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.43',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(f'https://servicos-cloud.saude.gov.br/pni-bff/v1/cidadao/cpf/{cpf}', headers=headers)
    data = response.json()
    if 'records' in data:
        record = data['records'][0] 
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

        context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Não foi possível consultar o CPF.")

def main():
    updater = Updater(token=6177077604:AAEoBC-JNywDBVT9cHZQwDSYk3gaCLRzSKU, use_context=True)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    cpf_handler = MessageHandler(Filters.text & ~Filters.command, consultar_cpf)
    dispatcher.add_handler(cpf_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()