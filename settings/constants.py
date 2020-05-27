import os
# # connection credentials

DB_URL='postgresql+psycopg2://anastas:password@0.0.0.0:5432/univer'

# DB_URL = os.environ['DB_URL']
# entities properties
USERS_FIELDS = ['id', 'name', 'email', 'phone']
MOVIE_FIELDS = ['id', 'name', 'year', 'genre', 'user_id']

# date of birth format
DATE_FORMAT = '%d.%m.%Y'

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]