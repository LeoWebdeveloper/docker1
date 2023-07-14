from fastapi import FastAPI, Path, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import pandas  as pd
from typing import Union



app = FastAPI( 
            title='Proyecto Individual - FastAPI - Docker',
            version="0.0.1",
            contact={
            "name": "Argumedo Héctor",
            "url": "https://github.com/ArgumedoHector",
            "email": "argalhec@gmail.com",},
            description = "En este proyecto pueden realizar distintas consultas con respecto a las plataformas Amazon, Disney, Hulu y netflix. 🚀"
            )

@app.on_event('startup')
def startup():
    global final_df
    final_df=pd.read_csv("final.csv")

@app.get("/")
async def index():
    return '''Henry PI - 01.\<br>
             
            /get_max_duration/{year}/{platform}/{tipo}
            /get_count_platform/{platform}
            /get_listedin/{genero}
            /get_actor/{platform}/{year} 

           '''


@app.get('/get_max_duration/{year}/{platform}/{tipo}')
def get_max_duration(year: int, platform: str, tipo: str):
    df3 = final_df[(final_df['release_year'] == year) & (final_df['Plataforma'] == platform)]
    if tipo == 'min':
        titulo = df3.loc[df3.movie_duration.idxmax()]['title']
    else:
        titulo = df3.loc[df3.seasson_quantity.idxmax()]['title']
    return {'titulo': titulo}

@app.get('/get_count_platform/{platform}')
def get_count_platform(platform: str):
    resultado1 = ((final_df['Plataforma'] == platform) & (final_df['type'].str.contains('Movie'))).sum()
    resultado2 = ((final_df['Plataforma'] == platform) & (final_df['type'].str.contains('TV Show'))).sum()
    return {
        'Plataforma': platform,
        'Movie': int(resultado1),
        'TV Show': int(resultado2)
    }




@app.get('/get_listedin/{genero}')
def get_listedin(genero:str):
    a=((final_df['listed_in'].str.contains(genero)) & (final_df['Plataforma']=='amazon')).sum()
    b=((final_df['listed_in'].str.contains(genero)) & (final_df['Plataforma']=='disney')).sum()
    c=((final_df['listed_in'].str.contains(genero)) & (final_df['Plataforma']=='hulu')).sum()
    d=((final_df['listed_in'].str.contains(genero)) & (final_df['Plataforma']=='netflix')).sum()
    lista=[a,b,c,d]
    resultado=max(lista)
    if a == resultado:
        plataforma='Amazon'
    if b == resultado:
        plataforma='Disney'
    if c == resultado:
        plataforma='Hulu'
    if d == resultado:
        plataforma='Netflix'
    return ( plataforma+'    '+str(resultado))


@app.get('/get_actor/{platform}/{year}')
def get_actor(platform:str, year:int):
    df2=final_df[(final_df['Plataforma']==platform) & (final_df['release_year']==year)]
    for i in df2['cast']:
        if i != 'Sin dato':
            i=i.replace(', ', ',')
        else:
            continue
    lista=[]
    for i in df2['cast']:
        if i != 'Sin dato':
            s=i.split(',')
            for j in range(len(s)):             
                if s[j] not in lista:
                    lista.append(s[j])
                else:
                    continue
        else:
            continue
    lista=list(set(lista))
    c=0
    dicc={}
    for i in lista:
        c=0
        for j in df2['cast']:
            if i in j.split(','):
                c+=1
        dicc[i]=c
    return (max(dicc, key=dicc.get), int(dicc[max(dicc, key=dicc.get)]))



