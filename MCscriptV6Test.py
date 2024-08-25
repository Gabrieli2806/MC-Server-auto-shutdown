import os
import time
import subprocess

# Ruta del archivo .jar del servidor
jar_file = r"C:\Users\User\OneDrive\MC - Server\MC-JB-Server\MC-JB-Server\ServerData\paper.jar"
# Ruta del archivo latest.log
log_file = r"C:\Users\User\OneDrive\MC - Server\MC-JB-Server\MC-JB-Server\ServerData\logs\latest.log"

# Variables para contar jugadores activos
OnlinePlayers = 0
jugadores_activos = set()

# Función para verificar el estado de los jugadores
def verificar_jugadores():
    global OnlinePlayers
    with open(log_file, 'r', encoding='utf-8', errors='ignore') as file:
        lines = file.readlines()
        for line in lines:
            if "joined the game" in line:
                # Extraer el nombre del jugador
                jugador = line.split()[3]
                if jugador not in jugadores_activos:
                    jugadores_activos.add(jugador)
                    OnlinePlayers += 1
            elif "left the game" in line:
                # Extraer el nombre del jugador
                jugador = line.split()[3]
                if jugador in jugadores_activos:
                    jugadores_activos.remove(jugador)
                    OnlinePlayers -= 1

# Directorio de la carpeta de los datos del servidor
os.chdir(r"C:\Users\User\OneDrive\MC - Server\MC-JB-Server\MC-JB-Server\ServerData")

# Verificar si el archivo .jar existe
if not os.path.exists(jar_file):
    print(f"Error: No se encontró el archivo java del server {jar_file}")
else:
    # Iniciar el servidor de Minecraft
    server_process = subprocess.Popen(['java', '-Xms16G', '-Xmx16G', '-jar', jar_file, '--nogui'], stdin=subprocess.PIPE, shell=True)

    # Revisar el archivo latest.log cada 5 segundos
    while True:
        time.sleep(300)  # tiempo de espera en segundos entre verificaciones
        verificar_jugadores()
        print("Jugadores Online: " + str(OnlinePlayers))
        
        # Si no hay jugadores activos, ejecutar comando y apagar el servidor
        if OnlinePlayers == 0:
            print("No hay jugadores activos. Iniciando secuencia de apagado...")
            server_process.stdin.write(b"say El servidor se apagara\n")
            server_process.stdin.write(b"stop\n")
            server_process.stdin.flush()
            time.sleep(30)  # Esperar un poco antes de apagar
            os.system("shutdown /s /t 1")