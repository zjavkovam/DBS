from django.shortcuts import render
from django.http import HttpResponse
import psycopg2

# Create your views here
from dbs_zadanie.settings import env


def message(request):
    SECRET_KEY = env('SECRET_KEY')
    conn = psycopg2.connect(
        host=env('DATABASE_HOST'),
        port=env('DATABASE_PORT'),
        database=env('DATABASE_NAME'),
        user=env('DATABASE_USER'),
        password=env('DATABASE_PASS')
    )

    cur = conn.cursor()

    poziadavka = "{\n  \"pgsql\": {\n      \"version\": \""
    cur.execute("SELECT VERSION();")
    poziadavka += cur.fetchone()[0] + "\",\n"
    cur.execute("SELECT pg_database_size('dota2')/1024/1024 as dota2_db_size;")
    poziadavka += "      \"dota2_db_size\": " + str(cur.fetchone()[0]) + "\n  }\n}"


    conn.commit()
    cur.close()
    conn.close()
    return HttpResponse(poziadavka)
