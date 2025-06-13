import os
import random
from flask import Flask, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import json
import time
from threading import Thread
from datetime import datetime

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Cargar datos
def load_data(filename):
    with open(f'data/{filename}') as f:
        return json.load(f)

matches = load_data('matches.json')
teams = load_data('teams.json')
team_stats = load_data('team_stats.json')
historical_data = load_data('historical_matches.json')

current_matches = {m['id']: m for m in matches if m['status'] == 'Live'}

# Endpoint para archivos estáticos
@app.route('/data/<path:path>')
def serve_data(path):
    return send_from_directory('data', path)

def simulate_match(match):
    """Simula eventos en un partido en vivo"""
    home_score, away_score = map(int, match['current_score'].split(':'))
    
    # Simular punto
    if random.random() > 0.3:
        if random.random() > match['odds']['home']:
            away_score += 1
        else:
            home_score += 1
    
    # Actualizar marcador
    match['current_score'] = f"{home_score}:{away_score}"
    
    # Verificar fin de set
    if home_score >= 25 or away_score >= 25:
        if abs(home_score - away_score) >= 2:
            match['sets'].append(match['current_score'])
            match['current_set'] += 1
            match['current_score'] = "0:0"
            
            # Verificar fin de partido
            home_sets = sum(1 for s in match['sets'] if int(s.split(':')[0]) > int(s.split(':')[1]))
            away_sets = sum(1 for s in match['sets'] if int(s.split(':')[0]) < int(s.split(':')[1]))
            
            if home_sets >= 3 or away_sets >= 3:
                match['status'] = "Finalizado"
                match['winner'] = "Brazil" if home_sets >= 3 else "Poland"
    
    # Actualizar estadísticas
    if match['status'] == 'Live':
        match['stats']['aces'][0] += random.randint(0, 1)
        match['stats']['aces'][1] += random.randint(0, 1)
        match['stats']['blocks'][0] += random.randint(0, 1)
        match['stats']['blocks'][1] += random.randint(0, 1)
        
        # Actualizar eficiencia de ataque
        for i in range(2):
            match['stats']['attackEff'][i] = max(0.2, min(0.7, 
                match['stats']['attackEff'][i] + random.uniform(-0.05, 0.05)))
    
    # Actualizar probabilidades
    total = home_score + away_score
    if total > 0:
        home_ratio = home_score / total
    else:
        home_ratio = 0.5
    
    match['odds']['home'] = max(0.1, min(0.9, home_ratio + random.uniform(-0.05, 0.05)))
    match['odds']['away'] = round(1 - match['odds']['home'], 2)
    
    return match

def simulate_live_matches():
    """Simula datos en vivo para partidos"""
    while True:
        for match_id in list(current_matches.keys()):
            match = current_matches[match_id]
            updated_match = simulate_match(match)
            
            # Emitir actualización
            socketio.emit('match_update', {
                'match_id': match_id,
                'data': updated_match
            })
            
            # Eliminar si finalizó
            if updated_match['status'] == 'Finalizado':
                del current_matches[match_id]
        
        time.sleep(5)

# Endpoints HTTP
@app.route('/api/teams')
def get_teams():
    return jsonify(teams)

@app.route('/api/matches')
def get_matches():
    return jsonify(matches)

@app.route('/api/matches/live')
def get_live_matches():
    return jsonify(list(current_matches.values()))

@app.route('/api/team-stats/<team_name>')
def get_team_stats(team_name):
    stats = team_stats.get(team_name, {})
    return jsonify(stats)

@app.route('/api/historical-matches')
def get_historical_matches():
    return jsonify(historical_data)

# WebSockets
@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')

@socketio.on('get_live_matches')
def handle_live_matches():
    emit('live_matches', list(current_matches.values()))

@socketio.on('subscribe_match')
def handle_subscribe_match(match_id):
    if match_id in current_matches:
        emit('match_data', current_matches[match_id])

if __name__ == '__main__':
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # Iniciar simulación en segundo plano
    Thread(target=simulate_live_matches, daemon=True).start()
    socketio.run(app, port=5000, debug=True)