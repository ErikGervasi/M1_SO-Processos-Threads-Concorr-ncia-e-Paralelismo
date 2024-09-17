import win32file, pywintypes
import time

# Função para receber dados do servidor
def receber_dados(pipe_name):
    pipe = None  # Inicializa a variável pipe como None
    try:
        while True:
            try:
                print(f"Conectando ao pipe {pipe_name}...")
                pipe = win32file.CreateFile(
                    pipe_name, 
                    win32file.GENERIC_READ, 
                    0, 
                    None, 
                    win32file.OPEN_EXISTING, 
                    0, 
                    None
                )
                break  # Sai do loop se a conexão foi bem-sucedida
            except pywintypes.error as e:
                if e.winerror == 231:  # Todas as instâncias de pipe estão ocupadas
                    print(f"Todas as instâncias de {pipe_name} estão ocupadas. Tentando novamente em 2 segundos...")
                    time.sleep(2)  # Espera 2 segundos antes de tentar novamente
                else:
                    print(f"Erro ao conectar ao pipe: {e}")
                    return  # Sai da função se o erro for outro
            
        while True:
            result, data = win32file.ReadFile(pipe, 1024)
            if data:
                message = data.decode('utf-8')
                print(f"Recebido do servidor: {message.strip()}")
                time.sleep(1)  # Simula o cliente esperando antes de fazer outra requisição
    except pywintypes.error as e:
        print(f"Erro durante a leitura do pipe: {e}")
    finally:
        if pipe:  # Verifica se o pipe foi criado antes de fechar
            win32file.CloseHandle(pipe)

if __name__ == "__main__":
    # Apresenta um menu interativo para o usuário escolher o tipo de cliente
    print("Escolha o tipo de cliente:")
    print("1 - Números")
    print("2 - Strings")
    escolha = input("Digite o número correspondente (1 ou 2): ")

    # Escolhe o pipe correto com base na escolha do cliente
    if escolha == '1':
        pipe_name = r'\\.\pipe\numeros_pipe'  # Conecta ao pipe de números
    elif escolha == '2':
        pipe_name = r'\\.\pipe\strings_pipe'  # Conecta ao pipe de strings
    else:
        print("Escolha inválida.")
        exit()

    # Simula o cliente fazendo requisições contínuas
    print("Iniciando cliente com requisições contínuas...")
    while True:
        receber_dados(pipe_name)
