# app.py
import os
import csv
import json
import numpy as np
from flask import Flask, render_template, request, jsonify
from datetime import datetime
from sklearn.linear_model import PoissonRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import RandomForestClassifier

app = Flask(__name__)

# Configuración de rutas de datos
DATA_DIR = "data"
TEAMS_FILE = os.path.join(DATA_DIR, "vnl_teams.json")
MATCHES_FILE = os.path.join(DATA_DIR, "vnl_matches.csv")
TEAM_STATS_DIR = os.path.join(DATA_DIR, "vnl_stats")

# Cargar datos de equipos
with open(TEAMS_FILE) as f:
    teams_data = json.load(f)

# Cargar datos de partidos históricos
matches = []
with open(MATCHES_FILE) as f:
    reader = csv.DictReader(f)
    for row in reader:
        matches.append(row)

def get_team_stats(team_name):
    """Obtiene estadísticas del equipo desde archivos locales"""
    try:
        team_file = os.path.join(TEAM_STATS_DIR, f"{team_name.lower().replace(' ', '_')}.json")
        with open(team_file) as f:
            return json.load(f)
    except:
        # Datos de respaldo si no se encuentra el archivo
        return {
            'win_rate': 0.55,
            'avg_points': 22.5,
            'avg_blocks': 8.2,
            'avg_aces': 2.1,
            'attack_success': 0.48,
            'reception_success': 0.62,
            'sets_won': 3.2,
            'sets_lost': 2.1
        }

def get_head_to_head(home_team, away_team):
    """Calcula historial de enfrentamientos desde datos históricos"""
    h2h = {
        'home_wins': 0,
        'away_wins': 0,
        'total_matches': 0,
        'avg_sets': 0,
        'avg_total_points': 0
    }
    
    total_sets = 0
    total_points = 0
    
    for match in matches:
        if match['home_team'] == home_team and match['away_team'] == away_team:
            h2h['total_matches'] += 1
            total_sets += int(match['home_sets']) + int(match['away_sets'])
            total_points += int(match['home_points']) + int(match['away_points'])
            
            if int(match['home_sets']) > int(match['away_sets']):
                h2h['home_wins'] += 1
            else:
                h2h['away_wins'] += 1
    
    if h2h['total_matches'] > 0:
        h2h['home_win_pct'] = (h2h['home_wins'] / h2h['total_matches']) * 100
        h2h['away_win_pct'] = (h2h['away_wins'] / h2h['total_matches']) * 100
        h2h['avg_sets'] = total_sets / h2h['total_matches']
        h2h['avg_total_points'] = total_points / h2h['total_matches']
    else:
        # Datos predeterminados si no hay historial
        h2h.update({
            'home_win_pct': 50,
            'away_win_pct': 50,
            'avg_sets': 4.2,
            'avg_total_points': 185
        })
    
    return h2h

def predict_match(home_team, away_team):
    """Realiza predicciones para el partido de vóleibol"""
    try:
        # Obtener estadísticas
        home_stats = get_team_stats(home_team)
        away_stats = get_team_stats(away_team)
        h2h_stats = get_head_to_head(home_team, away_team)
        
        # Preparar características para el modelo
        features = np.array([
            home_stats['win_rate'],
            home_stats['avg_points'],
            home_stats['attack_success'],
            away_stats['win_rate'],
            away_stats['avg_points'],
            away_stats['reception_success'],
            h2h_stats['home_win_pct'] / 100,
            h2h_stats['avg_total_points'] / 100
        ]).reshape(1, -1)
        
        # Modelo para predecir sets ganados
        model = make_pipeline(StandardScaler(), PoissonRegressor())
        
        # Datos de entrenamiento simulados (en producción usar histórico real)
        X_train = np.random.rand(100, 8)
        y_home_sets = np.random.poisson(lam=2.5, size=100)
        y_away_sets = np.random.poisson(lam=2.0, size=100)
        
        model.fit(X_train, y_home_sets)
        pred_home_sets = model.predict(features)[0]
        
        model.fit(X_train, y_away_sets)
        pred_away_sets = model.predict(features)[0]
        
        # Ajustar predicciones
        total_sets = pred_home_sets + pred_away_sets
        if total_sets > 5:
            adjustment = 5 / total_sets
            pred_home_sets *= adjustment
            pred_away_sets *= adjustment
        
        # Predecir ganador
        home_win_prob = home_stats['win_rate'] * 0.7 + h2h_stats['home_win_pct'] * 0.3
        away_win_prob = away_stats['win_rate'] * 0.7 + h2h_stats['away_win_pct'] * 0.3
        
        # Normalizar probabilidades
        total_prob = home_win_prob + away_win_prob
        home_win_pct = (home_win_prob / total_prob) * 100
        away_win_pct = (away_win_prob / total_prob) * 100
        
        # Generar análisis
        analysis = generate_analysis(home_stats, away_stats, h2h_stats)
        
        # Predecir otros mercados
        total_points = (home_stats['avg_points'] + away_stats['avg_points']) * 4.5
        both_win_set = "Sí" if min(pred_home_sets, pred_away_sets) >= 1 else "No"
        
        predictions = {
            'home_team': home_team,
            'away_team': away_team,
            'predicted_sets': f"{round(pred_home_sets)}-{round(pred_away_sets)}",
            'match_winner': home_team if home_win_pct > away_win_pct else away_team,
            'probability_home': round(home_win_pct),
            'probability_away': round(away_win_pct),
            'predicted_total_points': round(total_points),
            'both_win_set': both_win_set,
            'predicted_aces': round((home_stats['avg_aces'] + away_stats['avg_aces']) * 4),
            'predicted_blocks': round((home_stats['avg_blocks'] + away_stats['avg_blocks']) * 4),
            'analysis': analysis
        }
        
        return predictions
    
    except Exception as e:
        return {"error": str(e)}

def generate_analysis(home_stats, away_stats, h2h_stats):
    """Genera análisis basado en estadísticas"""
    analysis = []
    
    # Análisis ofensivo
    if home_stats['attack_success'] > 0.5:
        analysis.append(f"- {home_stats['name']} tiene un ataque potente ({home_stats['attack_success']*100}% de efectividad)")
    elif home_stats['attack_success'] < 0.4:
        analysis.append(f"- {home_stats['name']} muestra debilidad en ataque ({home_stats['attack_success']*100}% de efectividad)")
    
    # Análisis defensivo
    if away_stats['reception_success'] < 0.6:
        analysis.append(f"- {away_stats['name']} tiene recepción débil ({away_stats['reception_success']*100}% de efectividad)")
    
    # Historial directo
    if h2h_stats['home_win_pct'] > 70:
        analysis.append(f"- Historial favorable al local: {h2h_stats['home_win_pct']}% de victorias")
    
    # Recomendaciones de apuestas
    if home_stats['win_rate'] > 0.7 and away_stats['win_rate'] < 0.4:
        analysis.append("💰 Recomendación: Apuesta fuerte por victoria local")
    elif abs(home_stats['win_rate'] - away_stats['win_rate']) < 0.1:
        analysis.append("💰 Recomendación: Apuesta por más de 4 sets")
    
    return "\n".join(analysis)

@app.route('/')
def index():
    return render_template('index.html', teams=teams_data['teams'], current_year=datetime.now().year)

@app.route('/predict', methods=['POST'])
def predict():
    home_team = request.form['home_team']
    away_team = request.form['away_team']
    
    result = predict_match(home_team, away_team)
    
    if 'error' in result:
        return render_template('error.html', error=result['error'])
    
    return render_template('result.html', prediction=result, current_year=datetime.now().year)

if __name__ == '__main__':
    app.run(debug=True)