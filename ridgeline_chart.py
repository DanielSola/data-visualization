import pandas as pd
from ridgeplot import ridgeplot
import matplotlib.pyplot as plt
import numpy as np

# https://www.kaggle.com/datasets/thedevastator/housing-prices-in-barcelona

# Cargar datos de alquiler en barcelona por barrio
data = pd.read_csv('./datasets/Barcelona_Fotocasa_HousingPrices.csv', usecols=['price', 'neighborhood'])

# Valores máximo y mínimo para descartar outliers
max_allowed_rent = 2000
min_allowed_rent = 300


# Eliminar valores extremos que afectan a la visualización y no son representativos
data = data[data['price'] < max_allowed_rent]
data = data[data['price'] > min_allowed_rent]


# Agrupar por barrio
neighborhood_prices = data.groupby('neighborhood')['price'].apply(list).to_dict()
neighborhood_labels = data['neighborhood'].values

# Precio medio por barrio
average_prices = { neigh: np.mean(prices) for neigh, prices in neighborhood_prices.items()}

# Ordenar según precio medio por barrio
sorted_neighborhoods = sorted(average_prices.keys(), key=lambda x: average_prices[x])

sorted_samples = [neighborhood_prices[neigh] for neigh in sorted_neighborhoods]

kde_points = np.linspace(min_allowed_rent, max_allowed_rent, 200)


fig = ridgeplot(
    samples=sorted_samples,
    bandwidth=60,
    kde_points=kde_points,
    colorscale="viridis",
    colormode="row-index",
    coloralpha=0.65,
    labels=sorted_neighborhoods,
    linewidth=2,
    spacing=0.5,
)

fig.update_layout(
    height=1200,
    width=1500,
    title_text='Precios del alquiler en Barcelona por distrito en 2021',
    xaxis_title_text = 'Precio mensual (€)',
    font_size=25,
    showlegend=False)


fig.write_image("./plots/barcelona_rent.png")
