from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
from .. import schemas, basemodel, oauth2
from ..database import Session, get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[schemas.GetPost])
def get_all_posts(datab: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                  limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    posts = datab.query(basemodel.Post)\
        .filter(basemodel.Post.title.contains(search))\
        .limit(limit).offset(skip).all()

    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.GetPost)
def create_post(n_post: schemas.PostCreate, datab: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    new_post = basemodel.Post(owner_id=current_user.id, **n_post.dict())
    datab.add(new_post)  # add the new post
    datab.commit()  # push the new changes into database
    datab.refresh(new_post)  # returning post from database

    return new_post


@router.get('/{post_id}', response_model=schemas.GetPost)
def get_post(post_id: int, datab: Session = Depends(get_db),
             current_user: int = Depends(oauth2.get_current_user)):
    post = datab.query(basemodel.Post).filter(basemodel.Post.id == post_id).first()
    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"post with {post_id} doesn't exist.")

    return post


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, datab: Session = Depends(get_db),
                current_user: id = Depends(oauth2.get_current_user)):
    post_query = datab.query(basemodel.Post).filter(basemodel.Post.id == post_id)
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
def update_post(post_id: int, post: schemas.PostCreate, datab: Session = Depends(get_db),
                current_user: id = Depends(oauth2.get_current_user)):
    post_query = datab.query(basemodel.Post).filter(basemodel.Post.id == post_id)
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