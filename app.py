from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Model load
model = pickle.load(open('regressor_model_.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':

        runs = int(request.form['runs'])
        wickets = int(request.form['wickets'])
        overs = float(request.form['overs'])
        runs_last_5 = int(request.form['runs_in_prev_5'])
        wickets_last_5 = int(request.form['wickets_in_prev_5'])
        
        batting_team = request.form['batting_team']
        bowling_team = request.form['bowling_team']

        temp_array = [runs, wickets, overs, runs_last_5, wickets_last_5]

        # 3. Batting Teams
        # Sequence: Chennai, Delhi, Kings XI, Kolkata, Mumbai, Rajasthan, RCB, Sunrisers
        bat_teams = [
            'Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab', 
            'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 
            'Royal Challengers Bangalore', 'Sunrisers Hyderabad'
        ]
        
        for team in bat_teams:
            if team == batting_team:
                temp_array.append(1)
            else:
                temp_array.append(0)

        # 4. Bowling Teams
        bowl_teams = [
            'Chennai Super Kings', 'Delhi Daredevils', 'Kings XI Punjab', 
            'Kolkata Knight Riders', 'Mumbai Indians', 'Rajasthan Royals', 
            'Royal Challengers Bangalore', 'Sunrisers Hyderabad'
        ]
        
        for team in bowl_teams:
            if team == bowling_team:
                temp_array.append(1)
            else:
                temp_array.append(0)

        # 5. Final Array
        data = np.array([temp_array])
        
        # Prediction
        my_prediction = int(model.predict(data)[0])
              
        return render_template('index.html', lower_limit = my_prediction-5, upper_limit = my_prediction+5)

if __name__ == '__main__':
    app.run(debug=True)
# Keep alive code for render
import threading
import time
import requests

def keep_alive():
    # Website link
    url = "https://iplscorepredictor-8hwm.onrender.com/" 
    while True:
        try:
            requests.get(url)
            print("Pinged successfully!")
        except:
            print("Ping failed.")
        # Har 14 minute mein ping karega (Render 15 min mein sota hai)
        time.sleep(14 * 60) 

# Isko background thread mein chalayein
threading.Thread(target=keep_alive, daemon=True).start()
