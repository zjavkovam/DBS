from django.shortcuts import render
from django.http import JsonResponse
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
    poziadavka = {}
    cur.execute("SELECT VERSION();")
    poziadavka["prva"] = cur.fetchone()[0]
    cur.execute("SELECT pg_database_size('dota2')/1024/1024 as dota2_db_size;")
    poziadavka["druha"] = str(cur.fetchone()[0])

    conn.commit()
    cur.close()
    conn.close()
    odpoved = JsonResponse(poziadavka)
    return odpoved


def prvy_endpoint(request):
    SECRET_KEY = env('SECRET_KEY')
    conn = psycopg2.connect(
        host=env('DATABASE_HOST'),
        port=env('DATABASE_PORT'),
        database=env('DATABASE_NAME'),
        user=env('DATABASE_USER'),
        password=env('DATABASE_PASS')
    )
    cur = conn.cursor()

    query = "WITH temp AS( SELECT name, CAST(EXTRACT(epoch from release_date) AS INT) AS patch_start_date, CAST(EXTRACT(epoch from LEAD(release_date,1) OVER(ORDER BY release_date ASC)) AS INT) AS patch_end_date FROM patches) SELECT patches.name as patch_version, patches.patch_start_date, patches.patch_end_date,  matches.id as match_id, CAST(ROUND(matches.duration/60.0,2) as FLOAT) as match_duration FROM temp patches LEFT JOIN matches ON matches.start_time > patches.patch_start_date AND matches.start_time <  patches.patch_end_date"
    cur.execute(query)
    output = cur.fetchall()
    patches = []

    for i in output:
        if len(patches) != 0 and i[0] == patches[-1]["patch_version"]:
            patches[-1]["matches"].append({"match_id": i[3], "duration": i[4]})
        else:
            patch = {}
            patch["patch_version"] = i[0]
            patch["patch_start_date"] = i[1]
            patch["patch_end_date"] = i[2]
            if i[3] is not None:
                patch["matches"] = [{"match_id": i[3], "duration": i[4]}]
            else:
                patch["matches"] = []
            patches.append(patch)

    vypisanie = {"patches": patches}
    return JsonResponse(vypisanie)


def druhy_endpoint(request, id):
    SECRET_KEY = env('SECRET_KEY')
    conn = psycopg2.connect(
        host=env('DATABASE_HOST'),
        port=env('DATABASE_PORT'),
        database=env('DATABASE_NAME'),
        user=env('DATABASE_USER'),
        password=env('DATABASE_PASS')
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
    SECRET_KEY = env('SECRET_KEY')
    conn = psycopg2.connect(
        host=env('DATABASE_HOST'),
        port=env('DATABASE_PORT'),
        database=env('DATABASE_NAME'),
        user=env('DATABASE_USER'),
        password=env('DATABASE_PASS')
    )
    cur = conn.cursor()

    query = "SELECT players.id, COALESCE(players.nick, 'unknown') as player_nick, heroes.localized_name as hero_localized_name, matches.id as match_id, COALESCE(game_objectives.subtype, 'NO_ACTION') as hero_action, COUNT(*) FROM players JOIN matches_players_details ON  players.id = matches_players_details.player_id JOIN heroes ON matches_players_details.hero_id=heroes.id JOIN matches ON matches_players_details.match_id=matches.id FULL OUTER JOIN game_objectives  ON matches_players_details.id = game_objectives.match_player_detail_id_1 where players.id = " + id + " GROUP BY players.id, heroes.localized_name, matches.id, game_objectives.subtype ORDER BY match_id"
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
    SECRET_KEY = env('SECRET_KEY')
    conn = psycopg2.connect(
        host=env('DATABASE_HOST'),
        port=env('DATABASE_PORT'),
        database=env('DATABASE_NAME'),
        user=env('DATABASE_USER'),
        password=env('DATABASE_PASS')
    )
    cur = conn.cursor()

    query = "SELECT players.id, COALESCE(players.nick, 'unknown') as player_nick, heroes.localized_name as hero_localized_name, matches.id as match_id, abilities.name as ability_name, COUNT(abilities) as count, MAX(ability_upgrades.level) as level FROM players JOIN matches_players_details ON players.id = matches_players_details.player_id JOIN heroes ON matches_players_details.hero_id=heroes.id JOIN matches ON matches_players_details.match_id=matches.id JOIN ability_upgrades ON matches_players_details.id = ability_upgrades.match_player_detail_id JOIN abilities ON ability_upgrades.ability_id = abilities.id where players.id =" + id + "GROUP BY players.id, heroes.localized_name, matches.id, abilities.name ORDER BY match_id"
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


def z5_prvy_endpoint(request, id):
    SECRET_KEY = env('SECRET_KEY')
    conn = psycopg2.connect(
        host=env('DATABASE_HOST'),
        port=env('DATABASE_PORT'),
        database=env('DATABASE_NAME'),
        user=env('DATABASE_USER'),
        password=env('DATABASE_PASS')
    )
    cur = conn.cursor()

    query = "WITH t AS (SELECT matches.id as match_id,  heroes.id as hero_id, heroes.localized_name as hero_name, items.id as item_id, items.name as item_name, COUNT(items) as count, (CASE WHEN matches_players_details.player_slot <= 4 THEN matches.radiant_win  WHEN matches_players_details.player_slot >= 128 THEN not matches.radiant_win END) as winner from matches JOIN matches_players_details ON matches.id = matches_players_details.match_id JOIN heroes ON matches_players_details.hero_id = heroes.id JOIN purchase_logs ON matches_players_details.id = purchase_logs.match_player_detail_id JOIN items ON purchase_logs.item_id = items.id where matches.id = "+id+" GROUP BY matches.id, heroes.localized_name, items.name, heroes.id, items.id, matches_players_details.player_slot ORDER BY heroes.localized_name, items.name) select * from(select match_id, hero_id, hero_name, item_id,item_name, count, winner, row_number() over  (partition by hero_name order by count desc,item_name) as rank from t) ranks where rank <=5 AND winner = true ORDER BY hero_id, rank"
    cur.execute(query)
    output = cur.fetchall()
    vypisanie = {"id": output[0][0], "heroes": []}

    hero = {}
    for i in output:
        if len(hero) != 0 and i[1] != hero["id"]:
            vypisanie["heroes"].append(hero)
            hero = {}
        if hero == {}:
            hero["id"] = i[1]
            hero["name"] = i[2]
            hero["top_purchases"] = []
        if hero != {}:
            hero["top_purchases"].append({"id": i[3], "name": i[4], "count": i[5]})
    vypisanie["heroes"].append(hero)
    return JsonResponse(vypisanie)