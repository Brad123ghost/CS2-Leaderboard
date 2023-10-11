from flask import Flask, render_template, request, url_for
import requests

class Player(object):
    def __init__(self, rank, name, score):
        self.rank = rank
        self.name = name
        self.score = score

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def index():
    return render_template("index.html", players="")

@app.route("/api/current", methods=["POST", "GET"])
def current_leader():
    url = "https://api.steampowered.com/ICSGOServers_730/GetLeaderboardEntries/v1?format=json&lbname=official_leaderboard_premier_"
    season = "season1"
    
    res = requests.get(url+season).json()
    
    return res

@app.route("/api/getleaderboard", methods=["POST", "GET"])
def getleaderboard():
    url = "https://api.steampowered.com/ICSGOServers_730/GetLeaderboardEntries/v1?format=json&lbname=official_leaderboard_premier_"
    
    if request.method =="POST":
        season = request.form["season"]
        region = request.form["region"]
        
        res = requests.get(url+season+ ("" if region=="global" else ("_" + region))).json()
        
        playerList =[]
        
        # playerData = res["result"]["entries"].json()
        
        # for player in playerData:
        #     rank = player["rank"]
        #     score = player["score"]
        #     name = player["name"]
        #     playerList.append(Player(rank, score, name))
        
        # return playerList
        # return str(res["result"]["entries"][0]["name"]) + "\n" + str(res["result"]["entries"][1]["name"])
    
        for temp in res["result"]["entries"]:
            # rank = temp["rank"]
            # score = temp["score"]
            # name = temp["name"]
            playerList.append(Player(temp["rank"], temp["name"], temp["score"] >> 15))
    
        return render_template("index.html", players=playerList,regionName=region)
        # return str(res["result"]["entries"])
    return "Invalid"

app.run(host="0.0.0.0", port=5000, debug=True)