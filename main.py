from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from router import user, article

tags_metadata = [
    {
        "name": "AUTH",
        "description": "인증, 등록 등을 다룹니다.",
    },
]

app = FastAPI(
    title="Ugeo API",
    openapi_tags=tags_metadata
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "PUT", "DELETE",
                   "PATCH"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(article.router)
