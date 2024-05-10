import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=f0876dce92dd28505b9ec945cb32c688'.format(movie_id))
    data = response.json()    
    return "https://image.tmdb.org/t/p/original/" + data['poster_path']

def recommend_by_genre(genre):
    genre_movies = movies[movies['genres'].apply(lambda x: genre.lower() in x.lower())]
    recommended_movies = genre_movies.sample(n=5)
    recommended_movies_posters = [fetch_poster(movie_id) for movie_id in recommended_movies['movie_id']]
    return list(recommended_movies['title']), recommended_movies_posters

def recommend_by_title(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommend_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

# Check if 'genres' column exists in the DataFrame, if not, load genre information separately
if 'genres' not in movies.columns:
    # Load genre information from another source or file
    # Assuming genres are stored as a list in the 'genres' column in the DataFrame
    # Update movies_dict to include 'genres' information
    # Example: movies_dict = { 'title': ['Movie 1', 'Movie 2', ...], 'genres': [['Action', 'Adventure'], ['Comedy'], ...] }
    pass

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommendation System')

genre = st.radio("Select a movie genre:", ('Action', 'Superhero', 'Comedy', 'Romance', 'Sci-fi'))
if st.button('Recommend'):
    if genre:
        names, posters = recommend_by_genre(genre)
    else:
        selected_movie_name = st.selectbox(
            'Please select a movie name from the list',
            movies['title'].values)
        names, posters = recommend_by_title(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])