import pandas as pd  # works with tables
import numpy as np   # numerical operations (arrays, math)
import pickle        # save and load objects like vectorizer and encoder
from sklearn.preprocessing import LabelEncoder   # converts text labels -> numbers
from sklearn.feature_extraction.text import TfidfVectorizer  # converts text -> numbers
from sklearn.model_selection import train_test_split  # splits data into train/test
from sklearn.metrics.pairwise import cosine_similarity  # better similarity than dot product
from tensorflow import keras  # used to build neural network model

# FILE PATHS 
DATA_PATH = "movies_cleaned.csv"  # dataset file
MODEL_PATH = "movie_model.keras"  # saved model which is trained
VECTORIZER_PATH = "vectorizer.pkl"  # saved TF-IDF
ENCODER_PATH = "encoder.pkl"  # saved label encoder


# TRAINING
def load_data():
    data = pd.read_csv(DATA_PATH)   # load dataset

    data = data.dropna(subset=["Overview", "Genre"])    # remove rows with missing values

    # INPUT
    data["text"] = (data["Overview"] + " " + data["Genre"]).str.lower()  # combine overview + genre to give model stronger learning signals

    # TARGET 
    data["target"] = data["Genre"].apply(lambda x: x.split(",")[0].strip())  # we take only the FIRST genre so model will predict with one label

    print(data[["text", "target"]].head())

    # convert genre labels into numbers
    encoder = LabelEncoder()
    data["target_encoded"] = encoder.fit_transform(data["target"])

    print(data[["target", "target_encoded"]].head())

    # VECTORIZATION: convert text into numerical vectors 
    vectorizer = TfidfVectorizer(
        max_features=1000,        # use top 1000 words
        ngram_range=(1, 2),       # include single words + word pairs
        stop_words='english'      # remove common words (the, is, etc.)
    )

    X = vectorizer.fit_transform(data["text"]).toarray()

    print("Shape of X:", X.shape)

    Y = data["target_encoded"]

    # TRAIN-TEST SPLIT 
    x_train, x_test, y_train, y_test = train_test_split(
        X, Y, test_size=0.2, random_state=42
    )

    print("Train shape:", x_train.shape)
    print("Test shape:", x_test.shape)

    # MODEL
    model = keras.Sequential([
        keras.layers.Dense(256, activation="relu", input_shape=(X.shape[1],)),
        keras.layers.Dropout(0.3),   # prevents overfitting (model memorizing data)
        keras.layers.Dense(128, activation="relu"),
        keras.layers.Dropout(0.3),
        keras.layers.Dense(len(data["target_encoded"].unique()), activation="softmax")  # output layer -> gives probability for each genre
    ])

    model.compile(
        optimizer="adam",  # adjusts weights efficiently
        loss="sparse_categorical_crossentropy",  # used for classification
        metrics=["accuracy"]  # track accuracy
    )

    # TRAIN
    model.fit(
        x_train, y_train,
        epochs=20,            
        batch_size=32,
        validation_split=0.2   
    )

    # EVALUATE
    loss, accuracy = model.evaluate(x_test, y_test)
    print("Test Loss:", loss)
    print("Test Accuracy:", accuracy)

    # SAVE 
    model.save(MODEL_PATH)

    with open(VECTORIZER_PATH, "wb") as f:
        pickle.dump(vectorizer, f)

    with open(ENCODER_PATH, "wb") as f:
        pickle.dump(encoder, f)

    print("Model and tools saved successfully!")

    return data


#  INFERENCE 
saved_model = None   #stores model in memory
saved_vectorizer = None
saved_encoder = None
movie_df = None
movie_vectors = None


def load_artifacts():
    global saved_model, saved_vectorizer, saved_encoder, movie_df, movie_vectors

    if saved_model is None:
        print("Loading model...")

        # load saved model
        saved_model = keras.models.load_model(MODEL_PATH)

        # load vectorizer
        with open(VECTORIZER_PATH, "rb") as f:
            saved_vectorizer = pickle.load(f)

        # load encoder
        with open(ENCODER_PATH, "rb") as f:
            saved_encoder = pickle.load(f)

        # load dataset
        movie_df = pd.read_csv(DATA_PATH)
        movie_df = movie_df.dropna(subset=["Overview", "Genre"])

        # same preprocessing as training
        movie_df["text"] = (movie_df["Overview"] + " " + movie_df["Genre"]).str.lower()

        # precompute vectors (VERY IMPORTANT) : makes recommendation fast
        movie_vectors = saved_vectorizer.transform(movie_df["text"]).toarray()

    return True


# RECOMMENDER 
def predict_movies(genre, mood, type):
    if not load_artifacts():
        return {"error": "Model not loaded"}

    mood_map = {
        "happy": "funny comedy",
        "sad": "emotional drama",
        "excited": "action thriller",
        "romantic": "love romance",
        "scared": "horror thriller"
    }

    mood_text = mood_map.get(mood.lower(), "")

    user_input = f"{genre} {mood_text} {type} story film"
    user_vec = saved_vectorizer.transform([user_input]).toarray()

    # FILTER BY USER GENRE
    filtered_df = movie_df[
        movie_df["Genre"].str.contains(genre, case=False)
    ]

    # fallback if empty
    if len(filtered_df) == 0:
        filtered_df = movie_df.copy()

    # vectorize filtered movies
    filtered_vectors = saved_vectorizer.transform(filtered_df["text"]).toarray()

    # similarity
    similarity = cosine_similarity(filtered_vectors, user_vec).flatten()

    top_indices = similarity.argsort()[-10:][::-1]

    recs = filtered_df.iloc[top_indices]

    # sort by rating
    recs = recs.sort_values(by="IMDB_Rating", ascending=False).head(5)

    results = []
    for _, row in recs.iterrows():
        results.append({
            "title": row["Series_Title"],
            "rating": row["IMDB_Rating"],
            "genre": row["Genre"]
        })

    return {
        "recommendations": results
    }


# MAIN 
if __name__ == "__main__":
    load_data()