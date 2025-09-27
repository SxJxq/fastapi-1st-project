from fastapi import FastAPI, Response, status, HTTPException
import schemas
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from typing import List




app = FastAPI()



#connecting to the database
while True:
    try:
        conn = psycopg2.connect(host='localhost',database='postgres',user='postgres',password='7364',cursor_factory=RealDictCursor)
        cur=conn.cursor()
        print("connected to database")
        break
    
    except Exception as error:
        print("error connecting to database")
        print("error:", error)
        time.sleep(2)




@app.get("/")
def root():
    return {"message": "mew!"}

#GET ALL POSTS
@app.get("/posts", response_model=List[schemas.Post])#from api to user
def get_posts(): #DATA VALIDATION, from user to api
    cur.execute("""SELECT * FROM posts""")
    posts=cur.fetchall()
    return posts




#CREATE ONE POST
@app.post("/posts", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate):# data validation
    cur.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,(post.title, post.content, post.published))
    new_post=cur.fetchone()
    conn.commit()
    return new_post

    #just making a habit!!

#GETTING ONE POST
@app.get("/posts/{id}", response_model=schemas.Post)
def get_one_post(id: int):
    cur.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    the_post=cur.fetchone()

    if the_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} wasnt found")
    
    return the_post


#DELETING A POST
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    deleted_post = cur.fetchone()
    conn.commit()

    
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} wasnt found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#UPDATING A POST
@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate):
    cur.execute("""UPDATE posts SET title = %s , content = %s , published = %s WHERE id = %s RETURNING * """, (post.title , post.content, post.published, id) )
    updated_post=cur.fetchone()
    conn.commit()

    if updated_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} wasnt found")
    return updated_post


