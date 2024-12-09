from fastapi import FastAPI,status,Body,HTTPException
from pydantic import BaseModel                             #базовая модель для удобного представления данных
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
async def create_message(message: User) -> User:
    if len(users) == 0:
        message.id = len(users) + 1
    else:
        message.id = users[-1].id+1
    users.append(message)
    return message

@app.put("/user/{user_id}/{username}/{age}")
async def update_message(user_id: int, username: str, age: int) -> User:
    try:
        for user_ in users:
            if user_.id == user_id:
                user_.username = username
                user_.age = age
                return user_
    except IndexError:
        raise HTTPException(status_code=404, detail="User was not found")

@app.delete("/user/{user_id}")
async def delete_message(user_id: int) -> User:
    try:
        for user_ in users:
            if user_.id == user_id:
                message = users[user_id-1]
                del users[user_id-1]
                return message                          #если такое сообщение не нашлось,
    except IndexError:                                                     #то срабатывает исключение
        raise HTTPException(status_code=404, detail="User was not found")
