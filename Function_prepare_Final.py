import os
import numpy as np
import matplotlib.pyplot as plt

# Definire il percorso base nel tuo PC
base_path = "C:/Users/User/Desktop/PJ_AI/dataset/"
output_path = "C:/Users/User/Desktop/PJ_AI/photo/"

# Ottenere tutti i file nella directory che corrispondono al pattern richiesto
files = os.listdir(base_path)

# Filtrare i file per tx0rx0 e tx1rx1
tx0rx0_files = sorted([f for f in files if "tx0rx0" in f])
tx1rx1_files = sorted([f for f in files if "tx1rx1" in f])

# Altezza delle finestre (125 righe per 5 secondi, nel caso fisiologico)
height = 125

# Decidere se usare una o due antenne:
use_single = 0  # 0 significa usare 2 antenne

# Iterare sui file corrispondenti
for tx0_file, tx1_file in zip(tx0rx0_files, tx1rx1_files):
    # Caricare i dati dai file numpy
    data = np.load(os.path.join(base_path, tx0_file))
    data1 = np.load(os.path.join(base_path, tx1_file))

    # Convertire le matrici complesse in magnitudini (norme)
    data_float = np.abs(data)[:,0:40]
    data1_float = np.abs(data1)[:,0:40]

    # Step 1: Dividere le matrici in sottomatrici di altezza = 125 righe (5 secondi per fisio)
    n_rows = data_float.shape[0]
    n_parts = n_rows // height  # Numero di sottomatrici con altezza 125

    # Se ci sono righe rimanenti, aggiungere una parte aggiuntiva
    if n_rows % height != 0:
        n_parts += 1

    # Creare le sottomatrici dividendo entrambe le matrici
    parts_data = [data_float[i * height:(i + 1) * height, :] for i in range(n_parts)]
    parts_data1 = [data1_float[i * height:(i + 1) * height, :] for i in range(n_parts)]

    # Step 2: Affiancare le parti corrispondenti e salvarle come figure
    for i, (part_data, part_data1) in enumerate(zip(parts_data, parts_data1)):
        if use_single:
            merged_part = part_data
        else:
            # Affiancare (orizzontalmente) le due parti
            merged_part = np.hstack((part_data, part_data1))  # Combinarle fianco a fianco

        # Creare una nuova figura per ogni parte affiancata
        plt.figure(figsize=(merged_part.shape[1] / 100, merged_part.shape[0] / 100), dpi=100)
        plt.imshow(merged_part, cmap='gray', aspect='auto')
        plt.axis('off')  # Rimuovere gli assi per una vista più pulita

        # Rimuovere "Utente1fisio_" e sostituire il primo "_" con "." prima di "POLI"
        # Essenziale per Edge Impulse in modo tale che le classi siano importate in modo automatico
        output_file_base = tx0_file.replace("Utente1fisio_", "").replace("_POLI", ".POLI").replace("_tx0rx0.npy", "")
        output_file = os.path.join(output_path, f"{output_file_base}_part{i+1}.png")

        # Salvare la figura affiancata
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # Regolare il layout per evitare spazi bianchi
        plt.savefig(output_file, bbox_inches='tight', pad_inches=0)
        plt.close()  # Chiudere la figura per evitare visualizzazione e risparmiare memoria

print("Elaboration completed!")
