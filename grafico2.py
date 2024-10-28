import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

data_path = './csvs'

num_usuarios = [10, 100, 1000]
spawn_rates = [1.0, 2.0, 3.0]

tipos_requisicao = {
    "/2024/10/28/post-com-texto-de-400-kb/": "post com texto de 400kb",
    "/wp-content/uploads/2024/10/1920x1080-Hd-Pictures-Download-1024x576.jpg": "post com imagem de 300kb",
    "/wp-content/uploads/2024/10/626311.jpg": "post com imagem de 1mb"
}

requisicoes_por_segundo = {
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
                    requisicoes_segundo = tipo_data["Requests/s"].mean()
                    requisicoes_por_segundo[tipo][spawn_rate].append(requisicoes_segundo)
                else:
                    requisicoes_por_segundo[tipo][spawn_rate].append(0) 
        else:
            print(f"Arquivo {filename} não encontrado.")
            for tipo in tipos_requisicao.keys():
                requisicoes_por_segundo[tipo][spawn_rate].append(0)

for tipo, label in tipos_requisicao.items():

    dados_por_spawn = requisicoes_por_segundo[tipo]
    fig, ax = plt.subplots(figsize=(10, 6))
    width = 0.25 

    x = np.arange(len(num_usuarios))  # valoers do numero de usuario

    # barras por taxa de spawn
    for i, (spawn_rate, dados) in enumerate(dados_por_spawn.items()):
        ax.bar(x + i * width, dados, width, label=f"Instância {spawn_rate} usuários/s")

    ax.set_xlabel("Número de Usuários")
    ax.set_ylabel("Requisições por Segundo")
    ax.set_title(f"Requisições por Segundo para '{label}' por Número de Usuários e Instância")
    ax.set_xticks(x + width)
    ax.set_xticklabels(num_usuarios)
    ax.legend(title="Instância (usuários/s)")
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)

    plt.tight_layout()
    plt.savefig(f"grafico_requisicoes_{label.replace(' ', '_')}.png")
    plt.close(fig)
