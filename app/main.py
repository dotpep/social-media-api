from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = Field(None, ge=1, le=5)


my_posts = [
    {
        "id": 1,
        "title": "title of post", 
        "content": "content of post"
    },
    {
        "id": 2,
        "title": "favorite food", 
        "content": "pizza and patatoes"
    }
]

#my_posts = [
#    Post(id=1, title="Post 1", content="Content of Post 1"),
#    Post(id=2, title="Post 2", content="Content of Post 2"),
#]


def find_post(id: int) -> list[dict]:
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id: int) -> int:
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get('/')
def root():
    return {"message": "Welcome to my API"}


@app.get('/posts')
def get_posts_list():
    return {"data": my_posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = len(my_posts) + 1
    my_posts.append(post_dict)
    print("Post Succecfully Created: ", post_dict)
    return {"data": post_dict}


@app.get('/posts/latest')
def get_latest_post():
    post = my_posts[len(my_posts)-1]
    return {"detail": post}


@app.get('/posts/{id}')
def get_post_detail(id: int):  # def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id=} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message": f"post with {id=} was not found"}
        
    return {"post_details": post}


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id=} was not found")
    
    post_dict = post.dict()
    post_dict['id'] = id
    my_posts[index] = post_dict
    
    return {"data": post_dict}


@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id=} was not found")
    
    print("Post Succecfully Deleted: ", my_posts.pop(index))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
