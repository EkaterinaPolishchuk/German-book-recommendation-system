import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(layout="wide")

scraped_books_df = pd.read_csv("scraped_books.csv")

cv = CountVectorizer(max_features=226)
vector = cv.fit_transform(scraped_books_df["description"].values.astype("U")).toarray()

def recommend_similar_books(books_name):
    """
    Recommends similar books based on the input book's name.

    Parameters:
    - books_name (str): The name of the book for which recommendations are needed.

    Displays the top 5 recommended books with their names and images.
    """
    # Find the index of the selected book in the DataFrame
    idx_book = scraped_books_df.index[scraped_books_df["name"] == books_name]

    # Calculate the cosine similarity between all books' descriptions
    similarity = cosine_similarity(vector)

    # Sort books by similarity to the selected book
    distance = sorted(
        list(enumerate(similarity[idx_book[0]])),
        reverse=True,
        key=lambda vector: vector[1])

    # Create a list to store the top 5 recommended books
    recommended_books = []

    # Retrieve the top 5 recommended books and add them to the recommend list
    for i in distance[0:5]:
        recommended_books.append(scraped_books_df.iloc[i[0]])

    # Create columns for displaying book names and images
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]

    for i, col in enumerate(columns):
        col.write(recommended_books[i]["name"])
        col.image(recommended_books[i]["image"])


st.title("Book Recommendation System")

selected_book = st.selectbox(
    "Select the name of your favorite book",
    scraped_books_df["name"],
    index=None)
if selected_book in scraped_books_df["name"].values:
    # Recommend books based on the selected book
    recommend_similar_books(selected_book)
