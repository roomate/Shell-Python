import subprocess

# Exécuter une commande système et capturer la sortie en temps réel
process = subprocess.Popen(['ls', '-l'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# Lire l'erreur standard
stderr = process.stderr.read()
print("Erreur standard:")
print(stderr)

# Attendre la fin du processus
process.wait()

for line in process.stdout:
    print(line, end='')

# Afficher le code de retour
print("Code de retour:", process.returncode)