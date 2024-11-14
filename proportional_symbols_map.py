from matplotlib.lines import Line2D
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import MultiPolygon, Polygon, Point
import geopandas as gpd
import numpy as np

# Cargar datos de coste de vida
cost_of_living_data = pd.read_csv('./datasets/cost_of_living_by_country.csv')

# Lista de paises europeos. Creada con ChatGPT. Prompt: Give me a list of countries in mainland europe, as an array in python.
mainland_europe_countries = [
    "Albania", "Andorra", "Austria", "Belarus", "Belgium", "Bosnia and Herzegovina", "Bulgaria",
    "Croatia", "Czech Republic", "Denmark", "Estonia", "Finland", "France", "Germany", "Greece",
    "Hungary", "Iceland", "Italy", "Kosovo", "Latvia", "Liechtenstein", "Lithuania", "Luxembourg",
    "Moldova", "Monaco", "Montenegro", "Netherlands", "North Macedonia", "Norway", "Poland",
    "Portugal", "Romania", "San Marino", "Serbia", "Slovakia", "Slovenia", "Spain", "Sweden",
    "Switzerland", "Ukraine", "Vatican City", "United Kingdom"
]

# Filtrar para tener datos sólo delos paises europeos
europe_data = cost_of_living_data[cost_of_living_data['Country'].isin(mainland_europe_countries)]

# Cargar mapa del mundo. Fuente: naturalearthdata.com
world = gpd.read_file('./datasets/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp')

# Filtrar mapa para que contenga sólo los países europeos definidoss
europe_gdf = world[world['NAME_EN'].isin(mainland_europe_countries)]

# Actualizar las áreas de Francia para tener sólo Francia continental.
france_gdf = world[world['NAME_EN'] == 'France']
france_multipolygon = france_gdf.geometry.values[0]
mainland_bbox = Polygon([(-5.0, 41.0), (8.0, 41.0), (8.0, 51.0), (-5.0, 51.0)]) # Poligono de Europa
mainland_polygons = [poly for poly in france_multipolygon.geoms if poly.intersects(mainland_bbox)] # Incluír solo areas dentro de Europa continental
france_gdf.geometry.values[0] = MultiPolygon(mainland_polygons)
europe_gdf[europe_gdf['NAME_EN'] == 'France'] = france_gdf # Actualizar valor


# Mergear datos cartograficos con los datos sobre coste de vida
europe_gdf = europe_gdf.set_index('NAME_EN').join(europe_data.set_index('Country'))

# Corregir la posición del Centroide de Noruega, ya que no queda bien centrado sobre el país.
europe_gdf['centroid'] = europe_gdf.geometry.centroid
europe_gdf.loc[europe_gdf['SOVEREIGNT'] == 'Norway', 'centroid'] = Point(8, 61) # Punto cercano a Oslo, céntrico

# Corregir la posición del Centroide de Reino unido, ya que no queda bien centrado sobre el país.
europe_gdf.loc[europe_gdf['SOVEREIGNT'] == 'United Kingdom', 'centroid'] = Point(-1.25, 52.3) # Punto cercano a Londres, céntrico


# Transformar los datos de Coste de vida para resaltar las diferencias. Se ajustan entre 2 y 20 y se elevan al cuadrado
# Esto permite que los markers tengan medidas claramente diferenciables en función del coste de vida. Sino se hace esto, quedan todos los marcadores casi iguales
min_marker_size, max_marker_size = 2, 20
min_cost_of_living = europe_gdf['Cost of Living Index'].min()
max_cost_of_living = europe_gdf['Cost of Living Index'].max()

europe_gdf['marker_size'] = np.interp(europe_gdf['Cost of Living Index'], (min_cost_of_living, max_cost_of_living), (min_marker_size, max_marker_size)) ** 2

background_color = "#DAFFED"
country_color = "#9BF3F0"
country_edge_color = "#4A0D67"
marker_color = "#D00000"

# Plot
fig, ax = plt.subplots(1, 1, figsize=(14, 12))  # You can adjust this if you want multiple subplots
fig.patch.set_facecolor(background_color)  # Set background color to blue

# Marcadores de leyenda
sizes = [10, 25, 50, 75, 100, 125]
scaled_sizes = np.interp(sizes, (min_cost_of_living, max_cost_of_living), (min_marker_size, max_marker_size)) ** 2
labels = ["10", "25", "50", "75", "100", "125"]

# Leyenda de tamaño de marcadores
for size, label in zip(scaled_sizes, labels):
    ax.scatter([], [], color=marker_color, s=size, label=f'Cost of Living: {label}')

# Plotear los datos
europe_gdf.plot(ax=ax, color=country_color, edgecolor='#4A0D67')
europe_gdf['centroid'].plot(ax=ax, color=marker_color, marker='o', markersize=europe_gdf['marker_size'])

# Esconder ejes y leyenda
plt.axis('off')
plt.legend(loc='upper left', handletextpad=1, labelspacing=1.25, borderpad = 1.5)
plt.savefig('./plots/cost_of_living_by_country.png')

