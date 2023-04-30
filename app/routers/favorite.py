from fastapi import APIRouter, Depends, HTTPException, status
from app.database import Session, get_db
from app import models, oauth2
from app.schema import favorite

router = APIRouter(
    prefix="/favorites",
    tags=["Favorite"]
)


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def favorite(favorite_status: favorite.FavoriteBase,
                   db: Session = Depends(get_db),
                   current_user: int = Depends(oauth2.get_current_user)):
    query = db.query(models.Favorite).filter(
        models.Favorite.post_id == favorite_status.post_id,
        models.Favorite.user_id == current_user.id)

    found = query.first()

    if favorite_status.dir:
        if found:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail=f"user {current_user.id} already favorite post {favorite_status.post_id}")

        new_favorite = models.Favorite(post_id=favorite_status.post_id,
                                       user_id=current_user.id)

        db.add(new_favorite)
        db.commit()
        return {"message": "Favorite successfully"}

    else:
        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Post {favorite_status.post_id} not found")
        query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Favorite successfully deleted"}
