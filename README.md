# ARSUES
Tool brute force
<img width="1116" height="471" alt="imagen" src="https://github.com/user-attachments/assets/26bc40d6-0813-4b46-b864-1d36301fd9f9" />
Herramienta ligera y automatizada en Python para auditorías de seguridad y pruebas de fuerza bruta en servicios SSH desarrollada por Mrx04programmer y adaptada por 4dm0n - Admmin


🚀 Características
- Escaneo automatizado: Detecta los puertos TCP abiertos en el objetivo utilizando nmap antes de iniciar la prueba.
- Gestión de errores mejorada: Ignora y omite correctamente los cortes de conexión por parte del servidor (Connection reset by peer, errores de lectura de banner de SSH) para evitar interrupciones innecesarias en el script.
- Métricas en tiempo real: Calcula el tiempo total estimado y el promedio por intento durante la ejecución.
- Interfaz colorida: Utiliza códigos de escape ANSI para una visualización limpia y dinámica en la terminal.

📋 Requisitos Previos

Asegúrate de tener instalado Python 3 junto con las siguientes dependencias:

    paramiko
<br>
    
    nmap (instalado en el sistema operativo y disponible en el $PATH)

Puedes instalar la librería de Python ejecutando:
Bash

pip install paramiko

⚙️ Uso

      Ejecuta el script desde la terminal pasando como argumentos el diccionario de usuarios, el diccionario de contraseñas y la dirección IP objetivo:

      python3 script.py <archivo_de_diccionario_usuarios> <archivo_de_diccionario_contraseñas> <IP>

Ejemplo:

      python3 script.py users.txt passwords.txt 192.168.1.100

Durante la ejecución, el script escaneará los puertos disponibles, te pedirá seleccionar el puerto SSH correspondiente (ej. 22) y comenzará a testear las combinaciones.
