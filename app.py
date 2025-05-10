from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os
import time
import uuid

app = Flask(__name__)
app.secret_key = 'supersecretkey'

if not os.path.exists('data'):
    os.makedirs('data')

LOG_FILE = 'data/user_logs.csv'

@app.before_request
def assign_session_id():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        session['page_enter_time'] = time.time()

@app.route('/')
def index():
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('safe_page'))
    return render_template('login.html')

@app.route('/safe')
def safe_page():
    session['page_enter_time'] = time.time()
    return render_template('safe_page.html', page_type='safe')

@app.route('/phish')
def phishing_page():
    session['page_enter_time'] = time.time()
    return render_template('phishing_page.html', page_type='phish')

@app.route('/leaderboard')
def leaderboard():
    if os.path.exists(LOG_FILE):
        df = pd.read_csv(LOG_FILE)
        user_groups = df.groupby('username')

        leaderboard = []
        for user, group in user_groups:
            total_actions = len(group)
            safe_actions = len(group[group['page_type'] == 'safe'])
            phish_actions = len(group[group['page_type'] == 'phish'])
            avg_time = round(group['time_on_page_sec'].mean(), 2)
            leaderboard.append({
                'username': user,
                'total': total_actions,
                'safe': safe_actions,
                'phish': phish_actions,
                'avg_time': avg_time
            })

        # Sort by total actions, descending
        leaderboard = sorted(leaderboard, key=lambda x: x['total'], reverse=True)[:10]
    else:
        leaderboard = []

    return render_template('leaderboard.html', leaderboard=leaderboard)


@app.route('/log', methods=['POST'])
def log_action():
    data = request.form
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    time_on_page = round(time.time() - session.get('page_enter_time', time.time()), 2)
    df = pd.DataFrame([{
        'timestamp': timestamp,
        'session_id': session['session_id'],
        'username': session.get('username', 'guest'),
        'page_type': data.get('page_type'),
        'action': data.get('action'),
        'element': data.get('element'),
        'time_on_page_sec': time_on_page
    }])
    try:
        if os.path.exists(LOG_FILE):
            df.to_csv(LOG_FILE, mode='a', header=False, index=False)
        else:
            df.to_csv(LOG_FILE, index=False)
    except PermissionError:
        backup_name = time.strftime("backup_%Y-%m-%d_%H-%M-%S.csv")
        backup_file = os.path.join('data', backup_name)
        df.to_csv(backup_file, index=False)
        print(f"⚠️ [Backup] Main log file locked. Data saved to {backup_file}")
    return 'Logged', 200

#run app

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
