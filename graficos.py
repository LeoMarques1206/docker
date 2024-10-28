import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

data_path = './csvs'  

num_usuarios = [10, 100, 1000]
spawn_rates = [1.0, 2.0, 3.0]

# Mapeamento dos tipos de requisição para rótulos mais amigáveis
tipos_requisicao = {
    "/2024/10/28/post-com-texto-de-400-kb/": "post com texto de 400kb",
    "/wp-content/uploads/2024/10/1920x1080-Hd-Pictures-Download-1024x576.jpg": "post com imagem de 300kb",
    "/wp-content/uploads/2024/10/626311.jpg": "post com imagem de 1mb"
}

# Inicializa um dicionário para armazenar os tempos de resposta para cada tipo
tempo_resposta_por_tipo = {
    tipo: {f"{n_usuarios} usuários": [] for n_usuarios in num_usuarios} 
    for tipo in tipos_requisicao.keys()
}

for n_usuarios in num_usuarios:
    for spawn_rate in spawn_rates:
        filename = f"{n_usuarios}-{spawn_rate}.csv"
        file_path = os.path.join(data_path, filename)
        
        if os.path.isfile(file_path):
            data = pd.read_csv(file_path)
            
            # Calcula a média do tempo de resposta para cada tipo de requisição
            for tipo in tipos_requisicao.keys():
                tipo_data = data[data["Name"] == tipo]
                if not tipo_data.empty:
                    media_resposta = tipo_data["Average Response Time"].mean()
                    tempo_resposta_por_tipo[tipo][f"{n_usuarios} usuários"].append(media_resposta)
                else:
                    tempo_resposta_por_tipo[tipo][f"{n_usuarios} usuários"].append(None)
        else:
            print(f"Arquivo {filename} não encontrado.")
            for tipo in tipos_requisicao.keys():
                tempo_resposta_por_tipo[tipo][f"{n_usuarios} usuários"].append(None)

# Gera um gráfico para cada tipo de requisição com o novo rótulo
for tipo, label in tipos_requisicao.items():
    tempos_por_usuarios = tempo_resposta_por_tipo[tipo]
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.25  

    x = np.arange(len(spawn_rates))
    for i, (usuario_label, tempos) in enumerate(tempos_por_usuarios.items()):
        ax.bar(x + i * width, tempos, width, label=usuario_label)

    ax.set_xlabel("Taxa de Spawn (usuários por segundo)")
    ax.set_ylabel("Tempo de resposta médio (s)")
    ax.set_title(f"Tempo de Resposta para '{label}' por Número de Usuários e Taxa de Spawn")
    ax.set_xticks(x + width)
    ax.set_xticklabels(spawn_rates)
    ax.legend(title="Número de Usuários")
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    # Salva o gráfico com o novo nome de arquivo
    plt.savefig(f"grafico_{label.replace(' ', '_')}.png")
    plt.close(fig)  # Fecha o gráfico para evitar sobrecarga
