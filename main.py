import uvicorn
from fastapi import FastAPI
from database import Base, engine
from routers import (health, users, login)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="User Authentication Operations",
        description="This project is a backend API developed using FastAPI and SQLAlchemy. It provides robust functionality for user authentication and management, including creating, updating, and deleting user accounts. The API also includes a health check endpoint to monitor its status.",
        version="1.0.0"
    )

app.include_router(users.router)
app.include_router(health.router)
app.include_router(login.router)



if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


