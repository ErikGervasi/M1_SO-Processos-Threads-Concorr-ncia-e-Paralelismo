import win32pipe, win32file, pywintypes
import random
import time
from concurrent.futures import ThreadPoolExecutor

# Lista de frases para enviar
frases = [
    "Aula de Sistemas Operacionais",
    "O código funcionou",
    "Teste mensagem aleatória"
]

# Função para atender clientes de números
def handle_numeros(pipe_name):
    try:
        pipe = win32pipe.CreateNamedPipe(
            pipe_name, 
            win32pipe.PIPE_ACCESS_OUTBOUND,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT, 
            10, 65536, 65536, 0, None)
        print(f"Esperando cliente (Números) no pipe {pipe_name}...")
        win32pipe.ConnectNamedPipe(pipe, None)  # Espera cliente conectar
        while True:
            time.sleep(random.randint(1, 3))
            num = random.randint(1, 100)
            message = f"Numero: {num}\n".encode('utf-8')
            win32file.WriteFile(pipe, message)  # Envia a mensagem através do pipe
            print(f"Enviado ao cliente de números: {num}")
    except pywintypes.error as e:
        print(f"Erro na conexão com o cliente de números: {e}")
    finally:
        win32pipe.DisconnectNamedPipe(pipe)
        win32file.CloseHandle(pipe) 

# Função para atender clientes de strings
def handle_strings(pipe_name):
    try:
        pipe = win32pipe.CreateNamedPipe(
            pipe_name, 
            win32pipe.PIPE_ACCESS_OUTBOUND,
            win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_WAIT, 
            10, 65536, 65536, 0, None)  
        print(f"Esperando cliente (Strings) no pipe {pipe_name}...")
        win32pipe.ConnectNamedPipe(pipe, None)  # Espera cliente conectar
        while True:
            time.sleep(random.randint(1, 3))  
            frase = random.choice(frases)
            message = f"String: {frase}\n".encode('utf-8')
            win32file.WriteFile(pipe, message)  # Envia a mensagem
            print(f"Enviado ao cliente de strings: {frase}")
    except pywintypes.error as e:
        print(f"Erro na conexão com o cliente de strings: {e}")
    finally:
        win32pipe.DisconnectNamedPipe(pipe)
        win32file.CloseHandle(pipe)

def servidor():
    print("Servidor rodando e esperando por conexões...")

    # Cria um pool de threads com base no número de clientes que o sistema deve suportar
    with ThreadPoolExecutor(max_workers=10) as executor:
        # O loop cria instâncias de pipes continuamente, permitindo múltiplos clientes
        while True:
            executor.submit(handle_numeros, r'\\.\pipe\numeros_pipe')  # Cria um pipe para números
            executor.submit(handle_strings, r'\\.\pipe\strings_pipe')  # Cria um pipe para strings

if __name__ == "__main__":
    servidor()
