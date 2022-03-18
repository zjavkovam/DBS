from django.shortcuts import render
from django.http import JsonResponse
import json
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

    poziadavka = {
        "prva": cur.fetchone()[0],
        "druha": str(cur.fetchone()[0])
    }

    conn.commit()
    cur.close()
    conn.close()
    return JsonResponse(poziadavka)
