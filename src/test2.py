import os
import time

# Créer un processus enfant
pid = os.fork()

flags = os.WEXITED | os.WSTOPPED

if pid == 0:
    # Code exécuté par le processus enfant
    print("Je suis le processus enfant avec PID:", os.getpid())
    time.sleep(5)  # Simuler un travail en cours
    print("Le processus enfant termine.")
else:
    # Code exécuté par le processus parent
    print("Je suis le processus parent avec PID:", os.getpid())
    print("Attente de la fin du processus enfant avec PID:", pid)

    # Attendre que le processus enfant termine
    pid, status = os.waitpid(pid, os.WUNTRACED)
    print("Le processus enfant avec PID", pid, "a terminé avec le statut:", status)
