#!/usr/bin/env python3
"""
🎮 CS2 Stats Collector - Grupo de Amigos
Coleta automaticamente suas estatísticas do CS2 e envia para banco compartilhado
"""

from flask import Flask, request
import json
from datetime import datetime
import requests

# ===================================================
# 🔧 CONFIGURAÇÃO - EDITE APENAS ESTAS LINHAS:
# ===================================================
SUPABASE_URL = "https://hvbokgfvpuiivterexmk.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imh2Ym9rZ2Z2cHVpaXZ0ZXJleG1rIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjE2MTAyMDcsImV4cCI6MjA3NzE4NjIwN30.osV1tWvxsGQewkX7VU3a25e5kz8vS-1bMXhqWTDNtI4"

# ===================================================
# 🚀 CÓDIGO PRINCIPAL (NÃO EDITAR)
# ===================================================
app = Flask(__name__)
player_sessions = {}

def salvar_no_supabase(dados_partida):
    """Envia dados para o banco compartilhado"""
    try:
        headers = {
            'apikey': SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/cs2_matches", 
            headers=headers, 
            json=dados_partida
        )
        
        if response.status_code == 201:
            print(f"[OK] SUCESSO: {dados_partida['player_name']} - {dados_partida['kills']}K/{dados_partida['deaths']}D enviado!")
            return True
        else:
            print(f"[ERRO] Supabase: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"[ERRO] Conexao: {e}")
        return False

@app.route('/', methods=['POST'])
def receber_dados_cs2():
    """Recebe dados do CS2"""
    data = request.get_json()
    
    if not data or 'player' not in data or 'match_stats' not in data['player']:
        return "ok", 200
    
    player = data['player']
    stats = player.get('match_stats', {})
    map_data = data.get('map', {})
    
    player_name = player.get('name', 'unknown')
    map_name = map_data.get('name', 'unknown')
    
    # Evita duplicatas
    session_key = f"{player_name}_{map_name}_{datetime.now().strftime('%Y%m%d')}"
    
    dados_atuais = {
        'player_name': player_name,
        'map': map_name,
        'kills': stats.get('kills', 0),
        'deaths': stats.get('deaths', 0),
        'assists': stats.get('assists', 0),
        'mvps': stats.get('mvps', 0),
        'score': stats.get('score', 0),
        'steamid': player.get('steamid', ''),
        'team': player.get('team', 'unknown'),
        'timestamp': datetime.now().isoformat()
    }
    
    # Controle de sessão
    if session_key not in player_sessions:
        player_sessions[session_key] = {
            'inicio': datetime.now(),
            'melhores_stats': dados_atuais.copy(),
            'salvo': False
        }
        print(f"[NOVO] PARTIDA: {player_name} em {map_name}")
    else:
        session = player_sessions[session_key]
        if dados_atuais['kills'] > session['melhores_stats']['kills']:
            session['melhores_stats'] = dados_atuais.copy()
    
    # Salva após 60 segundos de jogo
    session = player_sessions[session_key]
    tempo_jogando = (datetime.now() - session['inicio']).total_seconds()
    
    if tempo_jogando > 60 and not session['salvo']:
        sucesso = salvar_no_supabase(session['melhores_stats'])
        if sucesso:
            session['salvo'] = True
            print(f"[SALVO] PARTIDA: {session['melhores_stats']['player_name']}")
    
    return "ok", 200

@app.route('/status')
def status():
    """Verifica se está funcionando"""
    return {
        'status': '[OK] Funcionando',
        'timestamp': datetime.now().isoformat(),
        'partidas_ativas': len(player_sessions),
        'supabase_ok': bool(SUPABASE_URL and SUPABASE_KEY)
    }

if __name__ == '__main__':
    print("=" * 60)
    print("CS2 Stats Collector - Iniciando...")
    print("=" * 60)
    
    # Verifica configuração
    if 'SEU_SUPABASE' in SUPABASE_URL or 'SUA_ANON' in SUPABASE_KEY:
        print("[ERRO] Configure SUPABASE_URL e SUPABASE_KEY!")
        input("Pressione Enter para sair...")
        exit(1)
    
    print(f"[OK] Banco configurado: {SUPABASE_URL}")
    print(f"[INFO] Servidor local: http://127.0.0.1:3000")
    print(f"[INFO] Status: http://127.0.0.1:3000/status")
    print("=" * 60)
    print("ABRA O CS2 E JOGUE! As stats serao coletadas automaticamente.")
    print("Para parar: Ctrl+C")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=3000, debug=False)