import pandas as pd
from pathlib import Path
import mlflow
import mlflow.sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


def load_data():
    path = Path("data") / "dataset_v2.csv"
    df = pd.read_csv(path, encoding="utf-8")
    print(f"Dataset cargado: {len(df)} registros")
    return df


def train_model(df):
    print("Entrenando modelo...")

    # Ajusta este campo si tu columna de texto tiene otro nombre
    text_column = "Descripcion"

    texts = df[text_column].fillna("").astype(str)

    vectorizer = TfidfVectorizer(max_features=2000)
    X = vectorizer.fit_transform(texts)

    model = KMeans(n_clusters=8, random_state=42)
    model.fit(X)

    return model, vectorizer


def save_model(model, vectorizer):
    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)

    model_path = models_dir / "kmeans_model.pkl"
    vect_path = models_dir / "vectorizer.pkl"

    pd.to_pickle(model, model_path)
    pd.to_pickle(vectorizer, vect_path)

    print("Modelo guardado en:", model_path)
    print("Vectorizador guardado en:", vect_path)


def main():
    mlflow.set_experiment("softland_hw_v2")

    with mlflow.start_run():
        df = load_data()
        model, vectorizer = train_model(df)

        save_model(model, vectorizer)

        mlflow.log_param("modelo", "KMeans")
        mlflow.log_param("clusters", 8)
        mlflow.log_param("max_features", 2000)

        print("Entrenamiento finalizado y registrado en MLflow.")


if __name__ == "__main__":
    main()
