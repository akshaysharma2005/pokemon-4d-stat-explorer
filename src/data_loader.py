import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

# Official Pokémon type color hex map
TYPE_COLORS = {
    "Grass": "#78C850",
    "Fire": "#F08030",
    "Water": "#6890F0",
    "Bug": "#A8B820",
    "Normal": "#A8A878",
    "Poison": "#A040A0",
    "Electric": "#F8D030",
    "Ground": "#E0C068",
    "Fairy": "#EE99AC",
    "Fighting": "#C03028",
    "Psychic": "#F85888",
    "Rock": "#B8A038",
    "Ghost": "#705898",
    "Ice": "#98D8D8",
    "Dragon": "#7038F8",
    "Dark": "#705848",
    "Steel": "#B8B8D0",
    "Flying": "#A890F0",
    "None": "#68A090"
}

# Type matchup chart (attacking -> defending: multiplier)
TYPE_EFFECTIVENESS = {
    "Normal":   {"Rock": 0.5, "Ghost": 0.0, "Steel": 0.5},
    "Fire":     {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 2.0, "Bug": 2.0, "Rock": 0.5, "Dragon": 0.5, "Steel": 2.0},
    "Water":    {"Fire": 2.0, "Water": 0.5, "Grass": 0.5, "Ground": 2.0, "Rock": 2.0, "Dragon": 0.5},
    "Electric": {"Water": 2.0, "Electric": 0.5, "Grass": 0.5, "Ground": 0.0, "Flying": 2.0, "Dragon": 0.5},
    "Grass":    {"Fire": 0.5, "Water": 2.0, "Grass": 0.5, "Poison": 0.5, "Ground": 2.0, "Flying": 0.5, "Bug": 0.5, "Rock": 2.0, "Dragon": 0.5, "Steel": 0.5},
    "Ice":      {"Fire": 0.5, "Water": 0.5, "Grass": 2.0, "Ice": 0.5, "Ground": 2.0, "Flying": 2.0, "Dragon": 2.0, "Steel": 0.5},
    "Fighting": {"Normal": 2.0, "Ice": 2.0, "Poison": 0.5, "Flying": 0.5, "Psychic": 0.5, "Bug": 0.5, "Rock": 2.0, "Ghost": 0.0, "Dark": 2.0, "Steel": 2.0, "Fairy": 0.5},
    "Poison":   {"Grass": 2.0, "Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0.0, "Fairy": 2.0},
    "Ground":   {"Fire": 2.0, "Electric": 2.0, "Grass": 0.5, "Poison": 2.0, "Flying": 0.0, "Bug": 0.5, "Rock": 2.0, "Steel": 2.0},
    "Flying":   {"Electric": 0.5, "Grass": 2.0, "Fighting": 2.0, "Bug": 2.0, "Rock": 0.5, "Steel": 0.5},
    "Psychic":  {"Fighting": 2.0, "Poison": 2.0, "Psychic": 0.5, "Dark": 0.0, "Steel": 0.5},
    "Bug":      {"Fire": 0.5, "Grass": 2.0, "Fighting": 0.5, "Poison": 0.5, "Flying": 0.5, "Psychic": 2.0, "Ghost": 0.5, "Dark": 2.0, "Steel": 0.5, "Fairy": 0.5},
    "Rock":     {"Fire": 2.0, "Ice": 2.0, "Fighting": 0.5, "Ground": 0.5, "Flying": 2.0, "Bug": 2.0, "Steel": 0.5},
    "Ghost":    {"Normal": 0.0, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5},
    "Dragon":   {"Dragon": 2.0, "Steel": 0.5, "Fairy": 0.0},
    "Dark":     {"Fighting": 0.5, "Psychic": 2.0, "Ghost": 2.0, "Dark": 0.5, "Fairy": 0.5},
    "Steel":    {"Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2.0, "Rock": 2.0, "Steel": 0.5, "Fairy": 2.0},
    "Fairy":    {"Fire": 0.5, "Fighting": 2.0, "Poison": 0.5, "Dragon": 2.0, "Dark": 2.0, "Steel": 0.5}
}

STAT_COLUMNS = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]

def load_pokemon_data(csv_path="data/pokemon.csv"):
    df = pd.read_csv(csv_path)
    df["Color"] = df["Type 1"].map(TYPE_COLORS).fillna("#A8A878")
    
    # Archetype Clustering using K-Means (5 clusters)
    X = df[STAT_COLUMNS]
    kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
    df["Cluster"] = kmeans.fit_predict(X)
    cluster_names = {
        0: "Physical Tank",
        1: "Special Sweeper",
        2: "Speed Striker",
        3: "Bulky Support",
        4: "Legendary Juggernaut"
    }
    df["Archetype"] = df["Cluster"].map(cluster_names)
    
    # 3D PCA coordinates for continuous manifold representation
    pca = PCA(n_components=3, random_state=42)
    pca_coords = pca.fit_transform(X)
    df["PCA_1"] = pca_coords[:, 0]
    df["PCA_2"] = pca_coords[:, 1]
    df["PCA_3"] = pca_coords[:, 2]
    
    return df, pca

def get_type_multiplier(attacker_type, defender_type1, defender_type2="None"):
    mult = 1.0
    if attacker_type in TYPE_EFFECTIVENESS:
        mult *= TYPE_EFFECTIVENESS[attacker_type].get(defender_type1, 1.0)
        if defender_type2 and defender_type2 != "None":
            mult *= TYPE_EFFECTIVENESS[attacker_type].get(defender_type2, 1.0)
    return mult
