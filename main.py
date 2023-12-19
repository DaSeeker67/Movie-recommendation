import streamlit as st
import pickle
import pandas as pd

import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=819be7176743b99cefa0459b42770e8d&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+ data['poster_path']




movies_list = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_list)
st.title('Which Movie to watch Next')
selected_movie = st.selectbox(
    'which movie you like the most ',
    movies['original_title'].values)



similarity = pickle.load(open('similarity.pkl', 'rb'))
def recommend(movie):
    movie_index = movies[movies['original_title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_poster = []

    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].original_title)
        recommended_poster.append(fetch_poster(movies.iloc[i[0]].id))
    return recommended_movies, recommended_poster

if st.button("Recommend"):
    names=[]
    posters =[]
    names, posters = recommend(selected_movie)
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