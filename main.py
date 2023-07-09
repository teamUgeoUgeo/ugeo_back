from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from router import user, article, comment

tags_metadata = [{
    "name": "AUTH",
    "description": "인증, 등록 등을 다룹니다.",
}, {
    "name": "Article",
    "description": "게시글 CRUD를 다룹니다."
}]

app = FastAPI(title="Ugeo API",
              openapi_tags=tags_metadata,
              docs_url='/api/docs',
              redoc_url='/api/redoc',
              openapi_url='/api/openapi.json')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(article.router)
app.include_router(comment.router)
