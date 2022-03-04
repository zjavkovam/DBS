from django.shortcuts import render
from django.http import HttpResponse
import psycopg2

# Create your views here
def message(request):
    conn = psycopg2.connect(
        host = "147.175.150.216",
        port="5432",
        database="dota2",
        user="xzjavkova",
        password="uVo.kur.2.esy"
    )

    cur = conn.cursor()

    cur.execute("SELECT VERSION();")
    poziadavka = cur.fetchone()
    cur.execute("SELECT pg_database_size('dota2')/1024/1024 as dota2_db_size;")

    conn.commit()
    cur.close()
    conn.close()
    return HttpResponse(poziadavka)
