import sys, requests, json

config = json.loads(open("config.json", "r").read())
API_KEY = config["key"]

def PLAYER_API(name, tag):
    return f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}?api_key={API_KEY}"
def SPECTATOR_API(puuid):
    return f"https://na1.api.riotgames.com/lol/spectator/v5/active-games/by-summoner/{puuid}?api_key={API_KEY}"

# information needed to spectate game
# Encyrption Key from spectator API and Game ID from spectator API
# cd /d "C:\Riot Games\League of Legends\Game" & "League of Legends.exe" "spectator spectator.na1.lol.pvp.net:8080 ENCRYPTIONKEY GAMEID NA1" "-UseRads"

def main(args):
    if len(args) > 1:
        player = args[1]
    else:
        player = input("Player name or puuid: ")

    if len(player) == 78: # length of puuid
        puuid = True
    else: 
        puuid = False

    if not puuid: # if input was a name
        if "#" not in player:
            tag = input("Input player tag: ")
        else:
            player, tag = player.split("#")
        player = player2puuid(player, tag)
    
    gameID, encryptKey = puuid2game(player)

    print("Paste the following into command prompt: ")
    commandstring1 = "cd /d \"C:\\Riot Games\\League of Legends\\Game\" & \"League of Legends.exe\" \"spectator spectator.na1.lol.pvp.net:8080"
    commandstring2 = "NA1\" \"-UseRads\""
    print(f"{commandstring1} {encryptKey} {gameID} {commandstring2}")

def player2puuid(name, tag):
    response = requests.get(PLAYER_API(name, tag))
    if response.ok:
        return response.json()["puuid"]
    else:
        print(f"Username {name}#{tag} Returned: {response.status_code}")
        exit()

def puuid2game(puuid):
    response = requests.get(SPECTATOR_API(puuid))
    if response.ok:
        responsejson = response.json()
        return responsejson["gameId"], responsejson["observers"]["encryptionKey"]
    else: 
        print(f"Spectator API Returned: {response.status_code}")
        exit()

main(sys.argv)