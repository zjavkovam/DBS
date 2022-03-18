from django.shortcuts import render
from django.http import JsonResponse
import json
import psycopg2

# Create your views here
from dbs_zadanie.settings import env


def message(request):
    conn = psycopg2.connect(
        host="147.175.150.216",
        port="5432",
        database="dota2",
        user="xzjavkova",
        password="uVo.kur.2.esy",
    )
    """
    SECRET_KEY = env('SECRET_KEY')
    conn = psycopg2.connect(
        host=env('DATABASE_HOST'),
        port=env('DATABASE_PORT'),
        database=env('DATABASE_NAME'),
        user=env('DATABASE_USER'),
        password=env('DATABASE_PASS')
    )
    """
    cur = conn.cursor()


    poziadavka = {

    }
    cur.execute("SELECT VERSION();")
    poziadavka["prva"] = cur.fetchone()[0]
    cur.execute("SELECT pg_database_size('dota2')/1024/1024 as dota2_db_size;")
    poziadavka["druha"] = str(cur.fetchone()[0])

    conn.commit()
    cur.close()
    conn.close()
    odpoved = JsonResponse(poziadavka)
    odpoved.status_code = 200
    return odpoved


def druhy_endpoint(request, id):
    conn = psycopg2.connect(
        host="147.175.150.216",
        port="5432",
        database="dota2",
        user="xzjavkova",
        password="uVo.kur.2.esy",
    )
    cur = conn.cursor()

    query = "SELECT players.id, COALESCE(players.nick, 'unknown') as player_nick, heroes.localized_name as hero_localized_name, CAST(ROUND(matches.duration/60.0,2) as FLOAT) as match_duration_minutes, COALESCE(matches_players_details.xp_hero,0) + COALESCE(matches_players_details.xp_creep,0) +  COALESCE(matches_players_details.xp_other,0) + COALESCE(matches_players_details.xp_roshan,0) as experiences_gained, matches_players_details.level as level_gained, matches.id as match_id, (CASE WHEN matches_players_details.player_slot <= 4 THEN matches.radiant_win WHEN matches_players_details.player_slot >= 128 THEN not matches.radiant_win END) as winner from players JOIN matches_players_details ON players.id = matches_players_details.player_id JOIN heroes ON matches_players_details.hero_id=heroes.id JOIN matches ON matches_players_details.match_id=matches.id where players.id =" + id + " ORDER BY match_id"
    cur.execute(query)
    output = cur.fetchall()
    vypisanie = {"id": output[0][0], "player_nick": output[0][1], "matches": []}

    for i in output:
        match = {}
        match["match_id"] = i[6]
        match["hero_localized_name"] = i[2]
        match["match_duration_minutes"] = i[3]
        match["experiences_gained"] = i[4]
        match["level_gained"] = i[5]
        match["winner"] = i[7]
        vypisanie["matches"].append(match)
    return JsonResponse(vypisanie)


def treti_endpoint(request, id):
    conn = psycopg2.connect(
        host="147.175.150.216",
        port="5432",
        database="dota2",
        user="xzjavkova",
        password="uVo.kur.2.esy",
    )
    cur = conn.cursor()

    query = "SELECT DISTINCT players.id, COALESCE(players.nick, 'unknown') as player_nick, heroes.localized_name as hero_localized_name, matches.id as match_id, COALESCE(game_objectives.subtype, 'NO_ACTION') as hero_action, COUNT(*) FROM players JOIN matches_players_details ON  players.id = matches_players_details.player_id JOIN heroes ON matches_players_details.hero_id=heroes.id JOIN matches ON matches_players_details.match_id=matches.id FULL OUTER JOIN game_objectives  ON matches_players_details.id = game_objectives.match_player_detail_id_1 where players.id = " + id + " GROUP BY players.id, heroes.localized_name, matches.id, game_objectives.subtype ORDER BY match_id"
    cur.execute(query)
    output = cur.fetchall()
    vypisanie = {"id": output[0][0], "player_nick": output[0][1], "matches": []}

    match = {}
    for i in output:
        if len(match) != 0 and i[3] != match["match_id"]:
            vypisanie["matches"].append(match)
            match = {}
        if match == {}:
            match["match_id"] = i[3]
            match["hero_localized_name"] = i[2]
            match["actions"] = []
        if match != {}:
            match["actions"].append({"hero_action": i[4], "count": i[5]})
    vypisanie["matches"].append(match)

    return JsonResponse(vypisanie)

def stvrty_endpoint(request, id):
    conn = psycopg2.connect(
        host="147.175.150.216",
        port="5432",
        database="dota2",
        user="xzjavkova",
        password="uVo.kur.2.esy",
    )
    cur = conn.cursor()

    query = "SELECT DISTINCT players.id, COALESCE(players.nick, 'unknown') as player_nick, heroes.localized_name as hero_localized_name, matches.id as match_id, abilities.name as ability_name, COUNT(abilities) as count, MAX(ability_upgrades.level) as level FROM players JOIN matches_players_details ON players.id = matches_players_details.player_id JOIN heroes ON matches_players_details.hero_id=heroes.id JOIN matches ON matches_players_details.match_id=matches.id JOIN ability_upgrades ON matches_players_details.id = ability_upgrades.match_player_detail_id JOIN abilities ON ability_upgrades.ability_id = abilities.id where players.id ="+id+"GROUP BY players.id, heroes.localized_name, matches.id, abilities.name ORDER BY match_id"
    cur.execute(query)
    output = cur.fetchall()
    vypisanie = {"id": output[0][0], "player_nick": output[0][1], "matches": []}

    match = {}
    for i in output:
        if len(match) != 0 and i[3] != match["match_id"]:
            vypisanie["matches"].append(match)
            match = {}
        if match == {}:
            match["match_id"] = i[3]
            match["hero_localized_name"] = i[2]
            match["abilities"] = []
        if match != {}:
            match["abilities"].append({"ability_name": i[4], "count": i[5], "upgrade_level": i[6]})
    vypisanie["matches"].append(match)

    return JsonResponse(vypisanie)