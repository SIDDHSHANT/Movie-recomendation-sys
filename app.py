import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np
st.set_page_config(page_title="Movie recomendation system",page_icon="https://www.google.com/imgres?q=movie%20icon%20image&imgurl=https%3A%2F%2Fwww.iconpacks.net%2Ficons%2F1%2Ffree-movie-icon-850-thumb.png&imgrefurl=https%3A%2F%2Fwww.iconpacks.net%2Ffree-icon%2Fmovie-850.html&docid=cPhsrnKf6O2HJM&tbnid=wUJmkqWSSwdIRM&vet=12ahUKEwibmf623NWXAxVjjOEIHbMoANIQnPAOegQIYBAA..i&w=512&h=512&hcb=2&ved=2ahUKEwibmf623NWXAxVjjOEIHbMoANIQnPAOegQIYBAA")


TMDB_API_KEY = "92edb2f6323fd5c6c9a1f7e349be2f2d"
def fetch_poster(movie_id):
    """Fetch movie poster from TMDB API."""

    url = f"https://api.themoviedb.org/3/movie/{movie_id}"

    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"

        return None

    except requests.exceptions.Timeout:
        st.warning("TMDB request timed out.")
        return None

    except requests.exceptions.ConnectionError:
        st.warning("Could not connect to TMDB. Check your internet connection.")
        return None

    except requests.exceptions.RequestException as e:
        st.warning(f"TMDB API error: {e}")
        return None

    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']
def recommend (movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1]) [1:6]

    recommended_movies = []
    recommended_movies_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id


        recommended_movies.append(movies.iloc[i[0]].title)
        # fetching poster from api
        poster = fetch_poster(movie_id)

        recommended_movies_poster.append(poster)
    return recommended_movies , recommended_movies_poster

movies_dict = pickle.load(open("movie_dict.pkl", "rb"))
movies =pd.DataFrame(movies_dict)



import streamlit as st
st.title("Movie Recommender System")
selected_movie_name = st.selectbox(
    "Select movie to recommend",
    movies["title"].values,
)
similarity = pickle.load(open("similarity.pkl", "rb"))
st.write("You selected:", selected_movie_name)

if st.button("Recommend"):

    names, posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.subheader(names[0])
        if posters[0] is not None:
            st.image(posters[0], use_container_width=True)
        else:
            st.write("Poster unavailable")

    with col2:
        st.subheader(names[1])
        if posters[1] is not None:
            st.image(posters[1], use_container_width=True)
        else:
            st.write("Poster unavailable")

    with col3:
        st.subheader(names[2])
        if posters[2] is not None:
            st.image(posters[2], use_container_width=True)
        else:
            st.write("Poster unavailable")

    with col4:
        st.subheader(names[3])
        if posters[3] is not None:
            st.image(posters[3], use_container_width=True)
        else:
            st.write("Poster unavailable")

    with col5:
        st.subheader(names[4])
        if posters[4] is not None:
            st.image(posters[4], use_container_width=True)
        else:
            st.write("Poster unavailable")