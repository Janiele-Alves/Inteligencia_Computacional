# -*- coding: utf-8 -*-
"""K-means_N2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1qMwS4_sz17D_s00N3w7wiyQqbX_SDICO
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from google.colab import drive
from collections import Counter

#Carregando os dados
drive.mount('/content/drive')
csv_path = '/content/drive/MyDrive/housing.csv'
data = pd.read_csv(csv_path)

from google.colab import drive
drive.mount('/content/drive')

print(data.head())

# Selecionar as colunas desejadas
df_cluster = data[['longitude', 'latitude', 'median_house_value', 'housing_median_age']]

# Visualizar as primeiras linhas dos dados selecionados
print(df_cluster.head())

# Normalização
df = pd.DataFrame(df_cluster)

# Selecionar apenas as colunas a serem normalizadas
colunas_para_normalizar = ['longitude', 'latitude', 'median_house_value', 'housing_median_age']
df_numerico = df[colunas_para_normalizar]

# Calcular a média e o desvio padrão
media = df_numerico.mean()
desvio_padrao = df_numerico.std()

# Normalizar os dados
df_normalizado = (df_numerico - media) / desvio_padrao

# Adicionar os dados normalizados de volta ao DataFrame original
df[colunas_para_normalizar] = df_normalizado

# Ver os primeiros dados normalizados
print(df)

df_cluster_scaled = df

def calcular_distancia(ponto1, ponto2):
    return np.sqrt(np.sum((ponto1 - ponto2) ** 2))

def kmeans_manual(data, k, max_iter=100):
    # Inicializar os centros dos clusters aleatoriamente
    np.random.seed(0)  # Para reprodutibilidade
    centros = data.sample(n=k).to_numpy()

    for _ in range(max_iter):
        # Passo 2: Atribuir cada ponto ao cluster mais próximo
        clusters = []
        for ponto in data.to_numpy():
            distancias = [calcular_distancia(ponto, centro) for centro in centros]
            cluster = np.argmin(distancias)
            clusters.append(cluster)

        # Passo 3: Recalcular os centros dos clusters
        novos_centros = []
        for i in range(k):
            pontos_cluster = data.to_numpy()[np.array(clusters) == i]
            if len(pontos_cluster) > 0:
                novo_centro = np.mean(pontos_cluster, axis=0)
                novos_centros.append(novo_centro)
            else:
                novos_centros.append(centros[i])  # Se não houver pontos, mantém o centro antigo

        novos_centros = np.array(novos_centros)

        # Verificar convergência
        if np.all(centros == novos_centros):
            break

        centros = novos_centros

    return clusters, centros

# Lista para armazenar o WCSS
wcss = []

# Testar o K-Means para valores de k de 2 a 10
for k in range(2, 11):
    clusters, centros = kmeans_manual(df_cluster_scaled, k)

    # Calcular WCSS
    wcss_value = 0
    for i in range(k):
        pontos_cluster = df_cluster_scaled.to_numpy()[np.array(clusters) == i]
        wcss_value += np.sum((pontos_cluster - centros[i]) ** 2)

    wcss.append(wcss_value)

# Exibir o WCSS para cada valor de k
print("WCSS para cada valor de k:")
for i, valor in enumerate(wcss, start=2):
    print(f"k={i}: {round(valor, 2)}")

# Plotar o gráfico do Método do Cotovelo (Elbow Method)
plt.figure(figsize=(10, 5))
plt.plot(range(2, 11), wcss, marker='o', linestyle='--')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of Clusters')
plt.ylabel('WCSS')
plt.grid(True)
plt.show()

"""O número ideal de clusters seria **4**, pois é o ponto onde o ganho em variabilidade explicada começa a diminuir, indicando que o uso de mais clusters não traria uma melhoria significativa em termos de compactação dos dados."""