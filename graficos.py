import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

data_path = './csvs'

num_usuarios = [10, 700, 1000]
spawn_rates = [1.0, 2.0, 3.0]

tipos_requisicao = {
    "/2024/10/28/post-com-texto-de-400-kb/": "post com texto de 400kb",
    "/wp-content/uploads/2024/10/1920x1080-Hd-Pictures-Download-1024x576.jpg": "post com imagem de 300kb",
    "/wp-content/uploads/2024/10/626311.jpg": "post com imagem de 1mb"
}

tempo_resposta_por_tipo = {
    tipo: {spawn_rate: [] for spawn_rate in spawn_rates} 
    for tipo in tipos_requisicao.keys()
}

for n_usuarios in num_usuarios:
    for spawn_rate in spawn_rates:
        filename = f"{n_usuarios}-{spawn_rate}.csv"
        file_path = os.path.join(data_path, filename)
        
        if os.path.isfile(file_path):
            data = pd.read_csv(file_path)
            
            for tipo in tipos_requisicao.keys():
                tipo_data = data[data["Name"] == tipo]
                if not tipo_data.empty:
                    media_resposta = tipo_data["Average Response Time"].mean()
                    tempo_resposta_por_tipo[tipo][spawn_rate].append(media_resposta)
                else:
                    tempo_resposta_por_tipo[tipo][spawn_rate].append(None)
        else:
            print(f"Arquivo {filename} não encontrado.")
            for tipo in tipos_requisicao.keys():
                tempo_resposta_por_tipo[tipo][spawn_rate].append(None)

# gera graficos
for tipo, label in tipos_requisicao.items():
    tempos_por_spawn = tempo_resposta_por_tipo[tipo]
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.25  

    x = np.arange(len(num_usuarios))  #numero de ususarios

    for i, (spawn_label, tempos) in enumerate(tempos_por_spawn.items()):
        ax.bar(x + i * width, tempos, width, label=f"Instancia {spawn_label}")

    ax.set_xlabel("Número de Usuários")
    ax.set_ylabel("Tempo de resposta médio (s)")
    ax.set_title(f"Tempo de Resposta para '{label}' por Número de Usuários e Instancia")
    ax.set_xticks(x + width)
    ax.set_xticklabels(num_usuarios)
    ax.legend(title="Instancia (usuários/s)")
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    plt.savefig(f"grafico_{label.replace(' ', '_')}.png")
    plt.close(fig)
