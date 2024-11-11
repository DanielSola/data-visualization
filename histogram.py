import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_histogram(file_path, column_name):
    data = pd.read_csv(file_path)

    plt.figure(figsize=(10, 6))
    plt.hist(data[column_name], bins=20, color='skyblue', edgecolor='black')
    plt.title('Histogram of IMDb Average Ratings')
    plt.xlabel('IMDb Average Rating')
    plt.ylabel('Frequency')
    plt.grid(axis='y', alpha=0.75)
    plt.savefig('./plots/film_ratings.png')

if __name__ == "__main__":
    csv_file_path = "./datasets/amazon_prime_films.csv"

    # Plot the histogram for 'imdbAverageRating' column
    plot_histogram(csv_file_path, 'imdbAverageRating')
