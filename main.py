from fastapi import FastAPI
import schemas
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()



#connecting to the database
conn = psycopg2.connect(
    host="localhost",
    database="fastapi",
    user="postgres",
    password="7364",
    cursor_factory=RealDictCursor
)
cur=conn.cursor()

@app.get("/")
def root():
    return {"message": "mew!"}

#GET ALL POSTS
@app.get("/posts")#from api to user
def get_posts(): #DATA VALIDATION, from user to api
    cur.execute("select * from posts")
    posts=cur.fetchall()
    return posts

#CREATE ONE POST
@app.post("/posts")
def create_post(post: dict):# turning json into python dictionarry
    cur.execute("insert into posts (title, content, published) values (%s, %s, %s) returning *",
                (post['title'], post['content'], post['published', True]))
    new_post=cur.fetchone()
    conn.commit()
    return new_post




