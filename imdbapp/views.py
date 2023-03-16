from django.shortcuts import render
from django.http import HttpResponse
import json
import http.client

# Create your views here.

def search(request):
    if request.method == 'POST':
        searched= request.POST.get ('search')

        conn = http.client.HTTPSConnection("imdb-movies-web-series-etc-search.p.rapidapi.com")

        headers = {
            'X-RapidAPI-Key': "d5aefcf253msh8a6c29baef0619bp197249jsn798c169e0085",
            'X-RapidAPI-Host': "imdb-movies-web-series-etc-search.p.rapidapi.com"
            }

        conn.request("GET", "/"+searched+".json", headers=headers)

        res = conn.getresponse()
        data = res.read()
        data=data.decode("utf-8")
        data= json.loads(data)
        data= data['d']
        
    return render(request,'search.html',{'items':data})

def imdbapp(request):
    

    conn = http.client.HTTPSConnection("imdb-top-100-movies.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "d5aefcf253msh8a6c29baef0619bp197249jsn798c169e0085",
        'X-RapidAPI-Host': "imdb-top-100-movies.p.rapidapi.com"
        }

    conn.request("GET", "/", headers=headers)

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data2= json.loads(data)

    context={'items':data2}
    return render(request,'index.html',context)

def movie(request, id):

    conn = http.client.HTTPSConnection("movies-tv-shows-database.p.rapidapi.com")

    headers = {
        'Type': "get-movie-details",
        'X-RapidAPI-Key': "d5aefcf253msh8a6c29baef0619bp197249jsn798c169e0085",
        'X-RapidAPI-Host': "movies-tv-shows-database.p.rapidapi.com"
        }

    conn.request("GET", "/?movieid="+id+"", headers=headers)

    res = conn.getresponse()
    data = res.read()
    data = data.decode("utf-8")
    data=json.loads(data)

    gen=data['genres']
    actors=data['stars'][:5]
    directors=data['directors'][:3]
    countries= data['countries']
    languages= data['language']

    conn = http.client.HTTPSConnection("imdb-movies-web-series-etc-search.p.rapidapi.com")

    headers = {
        'X-RapidAPI-Key': "d5aefcf253msh8a6c29baef0619bp197249jsn798c169e0085",
        'X-RapidAPI-Host': "imdb-movies-web-series-etc-search.p.rapidapi.com"
        }

    conn.request("GET", "/"+id+".json", headers=headers)

    res = conn.getresponse()
    img= res.read()
    img=img.decode("utf-8")
    img=json.loads(img)
    img=img['d'][0]['i']['imageUrl']

    return render(request,'movie.html',{'movie':data ,'gen':gen,'actors':actors,'directors':directors, 'countries':countries,'languages':languages,'img':img})