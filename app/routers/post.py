from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from app import models, oauth2
from app.database import Session, get_db
from app.schema import posts

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[posts.GetPost])
async def get_all_posts(datab: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                        limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    post = datab.query(models.Post) \
        .filter(models.Post.title.contains(search)) \
        .limit(limit).offset(skip).all()

    return post


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=posts.GetPost)
async def create_post(n_post: posts.PostCreate, datab: Session = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **n_post.dict())
    datab.add(new_post)  # add the new post
    datab.commit()  # push the new changes into database
    datab.refresh(new_post)  # returning post from database

    return new_post


@router.get('/{post_id}', response_model=posts.GetPost)
async def get_post(post_id: int, datab: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    post = datab.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"post with {post_id} doesn't exist.")

    return post


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, datab: Session = Depends(get_db),
                      current_user: id = Depends(oauth2.get_current_user)):
    post_query = datab.query(models.Post).filter(models.Post.id == post_id)
    deleted_post = post_query.first()

    if not deleted_post:  # check if there is not matched id
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"post with {post_id} doesn't exist.")
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail="Action is Unauthorized")

    post_query.delete(synchronize_session=False)
    datab.commit()  # push the new changes into database

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{post_id}')
async def update_post(post_id: int, post: posts.PostCreate, datab: Session = Depends(get_db),
                      current_user: id = Depends(oauth2.get_current_user)):
    post_query = datab.query(models.Post).filter(models.Post.id == post_id)
    updated_post = post_query.first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {post_id} doesn't exist.")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN,
                            detail="Action is Unauthorized")

    post_query.update(post.dict(), synchronize_session=False)
    datab.commit()  # push the new changes into database

    return post_query.first()
