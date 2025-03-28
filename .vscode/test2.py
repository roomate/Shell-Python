import os
import signal
import time

def child_process():
    print("Je suis le processus enfant avec PID:", os.getpid())
    # Simuler une tâche en cours d'exécution
    time.sleep(2)
    print("Processus enfant en cours d'exécution...")
    # Arrêter le processus enfant
    os.kill(os.getpid(), signal.SIGINT)
    print("Processus enfant arrêté (ce message ne sera pas affiché)")

# Créer un processus enfant
pid = os.fork()

if pid == 0:
    child_process()
else:
    # Code exécuté par le processus parent
    print("Je suis le processus parent avec PID:", os.getpid())

    # Attendre le processus enfant avec le flag WUNTRACED
    while True:
        try:
            pid, status = os.waitpid(pid, os.WUNTRACED)
            if os.WIFSTOPPED(status):
                print(f"Processus enfant {pid} arrêté par un signal")
                break
        except KeyboardInterrupt:
            print("Interruption par l'utilisateur")
            break

    # Continuer l'exécution du processus parent
    print("Processus parent continue l'exécution")
