from http import HTTPStatus

from fastapi import FastAPI

from fastapi_zero.routers import auth, users
from fastapi_zero.schemas import Message

app = FastAPI()

app.include_router(auth.router)
app.include_router(users.router)


@app.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=Message,
)
def read_root():
    return {'message': 'Olá mundo!'}


# Exercício 01
# @app.get('/olamundo', response_class=HTMLResponse)
# def ola_mundo():
#     return """
#         <html>
#         <head>
#         <title>Desafio Aula 2</title>
#         </head>
#         <body>
#         <h1> Olá mundo! </h1>
#         </body>
#         </html>"""
