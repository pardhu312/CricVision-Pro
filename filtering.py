import json
import pandas as pd 

All_batting=[]
All_bowling=[]
All_partnership=[]
All_matches=[]


def Batting_Score(batting_innings):
    
    Batter=[] 
    Score=[]
    total_runs=0
    total_extras=0
    Sixs=[]
    Fours=[]
    status={}
    before_ball=None
    Dots=[]
    Partnerships={}
    partnership_runs=0
    partnership_balls=0
    for over in match["innings"][batting_innings]["overs"]:
        for delivery in over["deliveries"]:
            if delivery["actual_delivery"] == before_ball and delivery["runs"]["batter"]==0:
                total_extras+=delivery["runs"]["extras"]  
            else:
                batter = delivery["batter"]
                non_striker = delivery["non_striker"]
                batter_score = delivery["runs"]["batter"]
                partnership_balls+=1
                partnership_runs += delivery["runs"]["total"]
                partnership = batter+ " & " +non_striker
                if "wickets" in delivery:
                    Partnerships[partnership]=(partnership_runs,partnership_balls)
                    partnership_runs=0
                    partnership_balls=0                    
                    for wicket in delivery["wickets"]:
                        status[wicket["player_out"]]= wicket["kind"]

                Batter.append(batter)
                Score.append(batter_score)
                dot = 1 if batter_score ==0 else 0 
                six = 1 if batter_score ==6 else 0
                four =1 if batter_score ==4 else 0
                Fours.append(four)
                Sixs.append(six)
                Dots.append(dot)
                total_runs+=delivery["runs"].get("total")
                total_extras+=delivery["runs"]["extras"]
                before_ball=delivery["actual_delivery"]
    Partnerships[partnership]=(partnership_runs,partnership_balls)            
    partnership_data=[]
    for pair, (runs, balls) in Partnerships.items():
        batter1, batter2 = pair.split(" & ")
        partnership_data.append({
            "Batter1": batter1,
            "Batter2": batter2,
            "Runs": runs,
            "Balls": balls
        })

    partnership_card= pd.DataFrame(partnership_data)            
    batting_card=pd.DataFrame({
        "Player":Batter,
        "Batter_Score":Score,
        "4s":Fours,
        "6s":Sixs,
        "Dots":Dots
            })  

    batting_card=batting_card.groupby("Player")[["Batter_Score","4s","6s","Dots"]].agg(Runs=("Batter_Score","sum"),Balls=("Batter_Score","count"),Fours=("4s","sum"),Sixs=("6s","sum"),Dots=("Dots","sum")).reset_index()
    batting_card["strike_rate"]=(batting_card["Runs"]/batting_card["Balls"])*100
    batting_card["status"]=batting_card["Player"].map(status).fillna("Not Out")
    batting_card["Date"] = date
    batting_card["Venue"] = venue
    batting_card["City"] = city
    batting_card["Result"] = result
    batting_card["Match_ID"] = match_id
    batting_card["Event"] = event
    batting_card["Toss_Winner"]=toss_winner
    batting_card["Player_of_match"]=[player_of_match]*len(batting_card)
    batting_card["Opponent"]=[opponent]*len(batting_card)

    partnership_card["Date"] = date
    partnership_card["Venue"] = venue
    partnership_card["City"] = city
    partnership_card["Result"] = result
    partnership_card["Match_ID"] = match_id
    partnership_card["Event"] = event
    partnership_card["Player_of_match"]=[player_of_match]*len(partnership_card)
    partnership_card["Opponent"]=[opponent]*len(partnership_card)
    return batting_card , partnership_card





def Bowling_Score(bowling_innings):
    Bowler=[]
    Runs=[]
    Wickets=[]
    Balls=[]
    maiden={}
    total_runs=0
    total_extras=0
    runs=0
    for over in match["innings"][bowling_innings]["overs"]:
        over_runs=0
        bowler=over["deliveries"][0]["bowler"]    
        if bowler not in maiden:
            maiden[bowler]=0   
        for delivery in over["deliveries"]:
            bowler=delivery["bowler"]
            Bowler.append(bowler)
            runs = delivery["runs"]["batter"]
            over_runs+=delivery["runs"]["total"]
            wicket=0
            if "wickets" in delivery:
                for w in delivery["wickets"]:
                    if w["kind"] not in ["run out", "retired hurt", "retired out"]:
                        wicket+=1
            Wickets.append(wicket)
            if "extras" in delivery and ("wides" in delivery["extras"] or "noballs" in delivery["extras"]):
                Balls.append(0)
                runs+=delivery["runs"]["extras"]
            else:
                Balls.append(1) 
            total_runs+=delivery["runs"].get("total")
            total_extras+=delivery["runs"]["extras"]  
            Runs.append(runs)
        if over_runs==0:
                maiden[bowler]+=1    
    bowling_card=pd.DataFrame({
        "Player":Bowler,
        "Runs":Runs,
        "Balls":Balls,
        "Wickets":Wickets
    })          
    bowling_card=bowling_card.groupby("Player")[["Runs","Balls","Wickets"]].agg(Runs=("Runs","sum"),Balls=("Balls","sum"),Wickets=("Wickets","sum")).reset_index()
    bowling_card["Overs"]=((bowling_card["Balls"]//6).astype(str)+"."+(bowling_card["Balls"]%6).astype(str))
    bowling_card["Economy"]=(bowling_card["Runs"]/(bowling_card["Balls"]/6)).round(2)
    bowling_card["Maidens"]=bowling_card["Player"].map(maiden)
    bowling_card["Date"] = date
    bowling_card["Venue"] = venue
    bowling_card["City"] = city
    bowling_card["Result"] = result
    bowling_card["Match_ID"] = match_id
    bowling_card["Event"] = event
    bowling_card["Player_of_match"]=[player_of_match]*len(bowling_card)
    bowling_card["Opponent"]=[opponent]*len(bowling_card)
    bowling_card["Toss_Winner"]=toss_winner

    return bowling_card


with open("india.json","r") as f:
    data=json.load(f)   

for match in data:
    batting_card=None
    bowling_card=None
    partnership=None
    innings=match.get("innings",[])
    team=match["info"].get("teams",[])
    if len(innings)>=2:
        if match["innings"][0]["team"]=="India":
            batting_innings=0    
            bowling_innings=1
        
        else:
            batting_innings=1
            bowling_innings=0  
    for item in team:
        if item!="India":
            opponent=item     
       

    player_of_match = None
    date = match["info"]["dates"][0]
    venue = match["info"]["venue"]
    city = match["info"].get("city", "")
    match_id = match["info"].get("match_type_number")
    outcome = match["info"]["outcome"]
    event = match["info"]["event"]["name"]
    toss_winner = match["info"]["toss"]["winner"]
    player_of_the_match = match["info"].get("player_of_match",[])
    player_of_match="".join(player_of_the_match)
    
    if "winner" in outcome:
        if outcome["winner"] == "India":
            result="Won"
        else:
            result="Lost"
    else:
        result=outcome.get("result","No result")  
    match_data = pd.DataFrame({
    "Match_ID": [match_id],
    "Date": [date],
    "Venue": [venue],
    "City": [city],
    "Opponent": [opponent],
    "Player_of_match": [player_of_match],
    "Event": [event],
    "Result": [result],
    "Toss_Winner": [toss_winner]
    })          

    if len(innings)> batting_innings:
        batting_card , partnership_card= Batting_Score(batting_innings)
    if len(innings) > bowling_innings:    
        bowling_card = Bowling_Score(bowling_innings)  

    if batting_card is not None: 
       All_batting.append(batting_card)
    if bowling_card is not None: 
        All_bowling.append(bowling_card)
    if partnership_card is not None: 
        All_partnership.append(partnership_card)
    All_matches.append(match_data)

batting_df=pd.concat(All_batting,ignore_index=True)
bowling_df=pd.concat(All_bowling,ignore_index=True)
partnership_df=pd.concat(All_partnership,ignore_index=True)
match_df=pd.concat(All_matches,ignore_index=True)

match_df.to_csv("Matches.csv",index=False)
batting_df.to_csv("Batting.csv",index=False)
bowling_df.to_csv("Bowling.csv",index=False)
partnership_df.to_csv("Partnership.csv",index=False)