from fastapi import FastAPI,status,Body,HTTPException
from pydantic import BaseModel                             #базовая модель дляудобногопредставления данных
from typing import List

app = FastAPI()

users = []                                                 #база данных

class User(BaseModel):                                  #каждое сообщение будет иметь:
    id: int = None                                      #номер пользователя
    username: str                                       #имя пользователя
    age: int                                            #возраст пользователя

@app.get("/users")
async def get_all_messages() -> List[User]:             #список объектов класса User
    return users                                        #возвращаем нашу базу данных

@app.post("/user/{username}/{age}")
async def create_message(message: User) -> str:
    message.id = len(users)
    users.append(message)
    return f"User {message} is registered"

@app.put("/user/{user_id}/{username}/{age}")
async def update_message(user_id: int, username: str, age: int) -> str:
    try:
        for user_ in users:
            if user_.id == user_id:
                user_.username = username
                user_.age = age
                return f"User {user_.id} has been updated"
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}")
async def delete_message(user_id: int) -> str:
    try:
        users.pop(user_id)
        return f"User {user_id} has been deleted"                          #если такое сообщение не нашлось,
    except IndexError:                                                     #то срабатывает исключение
        raise HTTPException(status_code=404, detail="User was not found")
