from fastapi import FastAPI, Request
from app import models
from app.database import engine
from app.routers import post, user, auth, favorite
from user_agents import parse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(favorite.router)


@app.get('/')
async def root():
    return {'message': 'Welcome to my API server'}


# @app.middleware("http")
# async def log_ip(request: Request, call_next):
#     user_agent = request.headers.get("User-Agent")
#     ua_string = str(user_agent)
#     user_agent_obj = parse(ua_string)
#     browser = user_agent_obj.browser.family
#     os = user_agent_obj.os.family
#     device = user_agent_obj.device.family
#     print(f"\n\n\n\n\nbrowser: {browser}, os: {os}, device: {device}\n\n\n\n\n")
#
#     response = await call_next(request)
#     return response