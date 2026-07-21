from flask import Flask,render_template
import pandas as pd
import plotly.express as px
app=Flask(__name__)
@app.route("/")
#---------------------------------home-page---------------------------------------------------------------
def home():
    players_info=pd.read_csv("players.csv")
    match_data=pd.read_csv("Matches.csv")
    opponents=match_data["Opponent"].drop_duplicates()
    player=players_info
    players_info=players_info[players_info["ID"].isin([50,34,9])]
    players_info=players_info.to_dict(orient="records")
    player=player.to_dict(orient="records")
    match_data=match_data.to_dict(orient="records")
    return render_template("home.html",players=players_info,player=player,match=match_data,opponents=opponents)
@app.route("/players")
#--------------------------------player-page--------------------------------------------------------------
def players():
    players_info=pd.read_csv("players.csv")
    players_info=players_info.to_dict(orient="records")
    return render_template("players.html",players=players_info)
@app.route("/players/<player_name>")
#----------------------------------player-profile----------------------------------------------------------
def players_profile(player_name):
    batting_df=pd.read_csv("Batting.csv")
    bowling_df=pd.read_csv("Bowling.csv")    
    player_info=pd.read_csv("players.csv")
    player=player_info[player_info["Player"]==player_name]
    if player.empty:
        return "Player not found", 404
    batters_run_against=(batting_df.groupby(["Player","Opponent"],as_index=False).agg(Runs=("Runs","sum"),No_of_Innings=("Runs","count"),No_of_NotOuts=("status",lambda x:(x=="Not Out").sum())).reset_index())
    batters_run_against["Batting_Avg"]=(batters_run_against["Runs"]/(batters_run_against["No_of_Innings"]-batters_run_against["No_of_NotOuts"])).round(2)
    bowlers_wickets_against=(bowling_df.groupby(["Player","Opponent"],as_index=False)["Wickets"].sum().reset_index())
    batter_run_against=batters_run_against[batters_run_against["Player"]==player_name].to_dict()
    bowler_wickets_against=bowlers_wickets_against[bowlers_wickets_against["Player"]==player_name].to_dict()
    batting_df["Date"]=pd.to_datetime(batting_df["Date"])
    batting_df["year"]=batting_df["Date"].dt.year
    year_runs=batting_df.groupby(["year","Player"]).agg(Runs=("Runs","sum")).reset_index()
    year_runs=year_runs[year_runs["Player"]==player_name].to_dict()
    bowling_df["Date"]=pd.to_datetime(bowling_df["Date"])
    bowling_df["year"]=bowling_df["Date"].dt.year
    year_wickets=bowling_df.groupby(["year","Player"]).agg(Wickets=("Wickets","sum")).reset_index()        
    year_wickets=year_wickets[year_wickets["Player"]==player_name].to_dict()
    bar_graph=None
    batting_stats=None
    avg_graph=None
    graph_runs=None
#-------------------------------------------for-batters-graphs------------------------------------------------------------------------    
    if not player.empty and player["Role"].iloc[0]!="Bowler":
        fig=px.line(    #-------------------runs-line-graph---------------------------------
            year_runs,
            x="year",
            y="Runs",
            title="Runs by year" ,
            text="Runs",
            markers=True
        )
        fig.update_layout(
            title={
                "text":"🏏  Runs by Year",
                "x":0.5
            },
            xaxis_title="Year",
            yaxis_title="Runs",
            font=dict(
                family="Arial",
                size=14,
                color="#1f2937"
            ),
            margin=dict(
                l=40,
                r=40,
                t=80,
                b=40
            ),
        paper_bgcolor="#6EADBC",
        plot_bgcolor="#6EADBC",
        showlegend=False,
        xaxis=dict(showgrid=False,zeroline=False),
        yaxis=dict(showgrid=False,zeroline=False)    
        )
        fig.update_traces(
            mode="lines+markers+text",
            line=dict(width=4,color="#2E7D32",shape="spline"),
            textposition="top center",
            cliponaxis=False
        )
        graph_runs=fig.to_html(full_html=False)        
        bar_graph=px.bar(     #---Runs graph----
            batter_run_against,
            x="Runs",
            y="Opponent",
            orientation="h",
            text="Runs"
        )
        bar_graph.update_layout(
            title={"text":"🏏 Run against each opponent","x":0.5},
            xaxis_title="Runs",
            yaxis_title="Opponenet",
        paper_bgcolor="#6EADBC",
        plot_bgcolor="#6EADBC",
        showlegend=False,
        xaxis=dict(showgrid=False,zeroline=False),
        yaxis=dict(showgrid=False,zeroline=False),
        barcornerradius="25%"   
        )
        bar_graph.update_traces(width=0.7, marker_color="#2E7D32",textposition="outside")
        bar_graph=bar_graph.to_html(full_html=False)
        avg_graph=px.bar(     #---Avg graph----
            batter_run_against,
            x="Batting_Avg",
            y="Opponent",
            orientation="h",
            text="Batting_Avg"
        )
        avg_graph.update_layout(
            title={"text":"🏏 Average against each opponent","x":0.5},
            xaxis_title="Batting_Avg",
            yaxis_title="Opponenet",
        paper_bgcolor="#6EADBC",
        plot_bgcolor="#6EADBC",
        showlegend=False,
        xaxis=dict(showgrid=False,zeroline=False),
        yaxis=dict(showgrid=False,zeroline=False),
        barcornerradius="25%"   
        )
        avg_graph.update_traces(width=0.7, marker_color="#2E7D32",textposition="outside")
        avg_graph=avg_graph.to_html(full_html=False)        
        batting_df["100s"]=batting_df["Runs"]>=100
        batting_df["50s"]=(batting_df["Runs"]>=50) & (batting_df["Runs"]<100)    
        batting_stats=batting_df.groupby("Player")[["Runs","Fours","Sixs","strike_rate","status","100s","50s"]].agg(Runs=("Runs","sum"),Fours=("Fours","sum"),Sixs=("Sixs","sum"),strike_rate=("strike_rate","mean"),No_of_Innings_bat=("Runs","count"),No_of_NotOuts=("status",lambda x:(x=="Not Out").sum()),Hundreds=("100s","sum"),Fifties=("50s","sum")).round(2).reset_index()
        batting_stats["Batting_Avg"]=(batting_stats["Runs"]/(batting_stats["No_of_Innings_bat"]-batting_stats["No_of_NotOuts"])).round(2)
        batting_stats["Boundaries"]=batting_stats["Fours"]+batting_stats["Sixs"]
        batting_stats=batting_stats[batting_stats["Player"]==player_name].iloc[0].to_dict()  
    bar_graph2=None 
    bowling_stats=None   
    graph_wickets=None
#------------------------------------for-bowler-graph------------------------------------------------------    
    if not player.empty and  player["Role"].iloc[0]!="Wicketkeeper Batter" and player["Role"].iloc[0]!="Batter":    
        fig=px.line(    #-------------------wickets-line-graph---------------------------------
            year_wickets,
            x="year",
            y="Wickets",
            title="Wickets by year" ,
            text="Wickets",
            markers=True
        )
        fig.update_layout(
            title={
                "text":" Wickets by Year",
                "x":0.5
            },
            xaxis_title="Year",
            yaxis_title="Wickets",
            font=dict(
                family="Arial",
                size=14,
                color="#1f2937"
            ),
            margin=dict(
                l=40,
                r=40,
                t=80,
                b=40
            ),
        paper_bgcolor="#6EADBC",
        plot_bgcolor="#6EADBC",
        showlegend=False,
        xaxis=dict(showgrid=False,zeroline=False),
        yaxis=dict(showgrid=False,zeroline=False)    
        )
        fig.update_traces(
            mode="lines+markers+text",
            line=dict(width=4,color="#2E7D32",shape="spline"),
            textposition="top center",
            cliponaxis=False
        )
        graph_wickets=fig.to_html(full_html=False)       
        bar_graph2=px.bar(     #-----wickets-graph---
            bowler_wickets_against,
            x="Wickets",
            y="Opponent",
            orientation="h",
            text="Wickets"      
        )
        bar_graph2.update_layout(
            title={"text":"🤾 Wickets against each opponent","x":0.5},
            xaxis_title="Wickets",
            yaxis_title="Opponent",
        paper_bgcolor="#6EADBC",
        plot_bgcolor="#6EADBC",
        showlegend=False,
        xaxis=dict(showgrid=False,zeroline=False),
        yaxis=dict(showgrid=False,zeroline=False),
        barcornerradius="25%"      
        )
        bar_graph2.update_traces(
            width=0.7,
            marker_color="#2E7D32",
            textposition="outside"        
            )        
        bar_graph2=bar_graph2.to_html(full_html=False)
        bowling_stats=bowling_df.groupby("Player")[["Runs","Wickets","Economy","Maidens"]].agg(Wickets=("Wickets","sum"),Economy=("Economy","mean"),Maidens=("Maidens","sum"),Five_Wts=("Wickets",lambda x:(x>=5).sum()),No_of_Innings_ball=("Runs","count"),Runs_condersed=("Runs","sum")).round(2).reset_index()
        bowling_stats["Bowling_Avg"]=(bowling_stats["Runs_condersed"]/bowling_stats["Wickets"]).round(2)
        bowling_stats=bowling_stats[bowling_stats["Player"]==player_name].iloc[0].to_dict()  
    player = player.to_dict(orient="records")[0]
    return render_template("player_profile.html",player=player,bar_graph=bar_graph,bar_graph2=bar_graph2,batting_stats=batting_stats,bowling_stats=bowling_stats,avg_graph=avg_graph,graph_runs=graph_runs,graph_wickets=graph_wickets)
@app.route("/dashboard")
#---------------------------------------------------dashbord----------------------------------------------------
def dashboard():
    batting_df=pd.read_csv("Batting.csv")
    players_info=pd.read_csv("players.csv")
    bowling_df=pd.read_csv("Bowling.csv")    
    match_data=pd.read_csv("Matches.csv")
    batting_df["Date"]=pd.to_datetime(batting_df["Date"])
    batting_df["year"]=batting_df["Date"].dt.year
    year_runs=batting_df.groupby("year").agg(Runs=("Runs","sum")).reset_index()
    bowling_df["Date"]=pd.to_datetime(bowling_df["Date"])
    bowling_df["year"]=bowling_df["Date"].dt.year
    year_wickets=bowling_df.groupby("year").agg(Wickets=("Wickets","sum")).reset_index()    
    batting_df["100s"]=batting_df["Runs"]>=100
    batting_df["50s"]=(batting_df["Runs"]>=50) & (batting_df["Runs"]<100)
    all_rounder=players_info[players_info["Role"]=="All-rounder"]
    batting_df=batting_df.groupby("Player")[["Runs","Fours","Sixs","strike_rate","status","100s","50s"]].agg(Runs=("Runs","sum"),Fours=("Fours","sum"),Sixs=("Sixs","sum"),strike_rate=("strike_rate","mean"),No_of_Innings_bat=("Runs","count"),No_of_NotOuts=("status",lambda x:(x=="Not Out").sum()),Hundreds=("100s","sum"),Fifties=("50s","sum")).round(2).reset_index()
    batting_df["Batting_Avg"]=(batting_df["Runs"]/(batting_df["No_of_Innings_bat"]-batting_df["No_of_NotOuts"])).round(2)
    batting_df["Boundaries"]=batting_df["Fours"]+batting_df["Sixs"]
    all_rounder_batting=batting_df[batting_df["Player"].isin(all_rounder["Player"])]
    bowling_df=bowling_df.groupby("Player")[["Runs","Wickets","Economy","Maidens"]].agg(Wickets=("Wickets","sum"),Economy=("Economy","mean"),Maidens=("Maidens","sum"),Five_Wts=("Wickets",lambda x:(x>=5).sum()),No_of_Innings_ball=("Runs","count"),Runs_condersed=("Runs","sum")).round(2).reset_index()
    bowling_df["Bowling_Avg"]=(bowling_df["Runs_condersed"]/bowling_df["Wickets"]).round(2)
    batter=batting_df.nlargest(1,"Runs").reset_index().iloc[0].to_dict()
    bowler=bowling_df.nlargest(1,"Wickets").reset_index().iloc[0].to_dict()
    all_rounder_bowling=bowling_df[bowling_df["Player"].isin(all_rounder["Player"])]
    all_rounder_performace=pd.merge(all_rounder_batting,all_rounder_bowling,how="left",on="Player")
    all_rounder_performace=all_rounder_performace.merge(players_info[["Player","Player_of_match"]],on="Player",how="left")
    all_rounder_performace["Score"]=(all_rounder_performace["Runs"]*25)+(all_rounder_performace["Batting_Avg"]*20)+(all_rounder_performace["strike_rate"]*10)+(all_rounder_performace["Wickets"]*25)-(all_rounder_performace["Economy"]*5)+(players_info["Player_of_match"]*5) 
    all_rounder_performace["rank"]=all_rounder_performace["Score"].rank(method="dense",ascending=False).astype(int)
    top_all_rounder=all_rounder_performace[all_rounder_performace["rank"]==1].iloc[0].to_dict()
    opponents=match_data["Opponent"].drop_duplicates()    
    fig=px.line(    #-------------------runs-line-graph---------------------------------
        year_runs,
        x="year",
        y="Runs",
        title="Runs by year" ,
        text="Runs",
        markers=True
    )
    fig.update_layout(
        title={
            "text":"🏏 India Runs by Year",
            "x":0.5
        },
        xaxis_title="Year",
        yaxis_title="Runs",
        font=dict(
            family="Arial",
            size=14,
            color="#1f2937"
        ),
        margin=dict(
            l=40,
            r=40,
            t=80,
            b=40
        ),
    paper_bgcolor="#6EADBC",
    plot_bgcolor="#6EADBC",
    showlegend=False,
    xaxis=dict(showgrid=False,zeroline=False),
    yaxis=dict(showgrid=False,zeroline=False)    
    )
    fig.update_traces(
        mode="lines+markers+text",
        line=dict(width=4,color="#2E7D32",shape="spline"),
        textposition="top center",
        cliponaxis=False
    )
    graph_runs=fig.to_html(full_html=False)
    fig=px.line(    #-------------------wickets-line-graph---------------------------------
        year_wickets,
        x="year",
        y="Wickets",
        title="Wickets by year" ,
        text="Wickets",
        markers=True
    )
    fig.update_layout(
        title={
            "text":"🏏 wickets by Year",
            "x":0.5
        },
        xaxis_title="Year",
        yaxis_title="wickets",
        font=dict(
            family="Arial",
            size=14,
            color="#1f2937"
        ),
        margin=dict(
            l=40,
            r=40,
            t=80,
            b=40
        ),
    paper_bgcolor="#6EADBC",
    plot_bgcolor="#6EADBC",
    showlegend=False,
    xaxis=dict(showgrid=False,zeroline=False),
    yaxis=dict(showgrid=False,zeroline=False)    
    )
    fig.update_traces(
        mode="lines+markers+text",
        line=dict(width=4,color="#2E7D32",shape="spline"),
        textposition="top center",
        cliponaxis=False
    )
    graph_wickets=fig.to_html(full_html=False)    
    
    top_batter=batting_df[batting_df["Player"]==batter["Player"]].iloc[0].to_dict()
    top_bowler=bowling_df[bowling_df["Player"]==bowler["Player"]].iloc[0].to_dict()
    top_10_batters=batting_df.nlargest(10,"Runs").to_dict()
    top_10_bowlers=bowling_df.nlargest(10,"Wickets").to_dict()
    bar_graph=px.bar(     #---top 10 Runs graph-------------------------------
        top_10_batters,
        x="Runs",
        y="Player",
        orientation="h",
        text="Runs"
    )
    bar_graph.update_layout(
        title={"text":"🏏 Top 10 Run Scorers","x":0.5},
        xaxis_title="Runs",
        yaxis_title="Players",
    paper_bgcolor="#6EADBC",
    plot_bgcolor="#6EADBC",
    showlegend=False,
    xaxis=dict(showgrid=False,zeroline=False),
    yaxis=dict(showgrid=False,zeroline=False),
    barcornerradius="25%"   
    )
    bar_graph.update_traces(width=0.7, marker_color="#2E7D32",textposition="outside")
    bar_graph=bar_graph.to_html(full_html=False)

    bar_graph2=px.bar(     #-----top 10 wickets-graph---------------------------------
        top_10_bowlers,
        x="Wickets",
        y="Player",
        orientation="h",
        text="Wickets"      
    )
    bar_graph2.update_layout(
        title={"text":"🤾Top 10 Wicket Takers","x":0.5},
        xaxis_title="Wickets",
        yaxis_title="Players",
    paper_bgcolor="#6EADBC",
    plot_bgcolor="#6EADBC",
    showlegend=False,
    xaxis=dict(showgrid=False,zeroline=False),
    yaxis=dict(showgrid=False,zeroline=False),
    barcornerradius="25%"      
    )
    bar_graph2.update_traces(
        width=0.7,
        marker_color="#2E7D32",
        textposition="outside"        
        )        
    bar_graph2=bar_graph2.to_html(full_html=False)
    win_pie=match_data.groupby("Result").size().reset_index(name="count")
    pie_chart = px.pie(   #----------------------------------wins-pie-chart---------------------------------
        win_pie,
        names="Result",
        values="count",
        title="Overall Match Results Summary",
        color="Result",
        color_discrete_map={
            "Won": "#85A947",        # Green
            "Lost": "#E74C3C",       # Red
            "Tie": "#FFDE4E",        # Yellow
            "No Result": "#DDDAD0"   # Gray
        }
    )
    pie_chart.update_traces(
        hole=0.3,
        textposition="outside",
        textinfo="label+value+percent"
    )
    pie_chart.update_layout(
        width=600,
        height=500,
        title_x=0.5,
        legend_title="Match Result",
        paper_bgcolor="#6EADBC",
        plot_bgcolor="#6EADBC",
        showlegend=False,
    )
    pie_chart=pie_chart.to_html(full_html=False)
    wins_per_opponent=match_data.groupby("Opponent").agg(wins=("Result",lambda x:(x=="Won").sum()),total_matches=("Result","count")).reset_index()
    wins_per_opponent["Win%"]=((wins_per_opponent["wins"]/wins_per_opponent["total_matches"])*100).round(2)
    wins_per_opponent["Text"] = (
    "Win%: " + wins_per_opponent["Win%"].astype(str) + "%" +
    "<br>Matches: " + wins_per_opponent["total_matches"].astype(str))
    bar_graph3=px.bar(     #-----wins-against-opponent-graph---
        wins_per_opponent,
        x="Win%",
        y="Opponent",
        orientation="h",
        text="Text"      
    )
    bar_graph3.update_layout(
        title={"text":"Winpercentage against each opponent 2021 - 2026","x":0.5},
        xaxis_title="Win%",
        yaxis_title="Opponents",
    paper_bgcolor="#6EADBC",
    plot_bgcolor="#6EADBC",
    showlegend=False,
    xaxis=dict(showgrid=False,zeroline=False),
    yaxis=dict(showgrid=False,zeroline=False),
    barcornerradius="25%"      
    )
    bar_graph3.update_traces(
        width=0.7,
        marker_color="#2E7D32",
        textposition="outside"
        )      
    bar_graph3=bar_graph3.to_html(full_html=False)    
    wins_per_venue=match_data.groupby("City").agg(wins=("Result",lambda x:(x=="Won").sum()),total_matches=("Result","count")).reset_index()
    wins_per_venue["Win%"]=((wins_per_venue["wins"]/wins_per_venue["total_matches"])*100).round(2)
    wins_per_venue["Text"] = (
    "Win%: " + wins_per_venue["Win%"].astype(str) + "%" +
    "<br>Matches: " + wins_per_venue["total_matches"].astype(str))
    bar_graph4=px.bar(     #-----wins-in-each-venue-graph-----------------------------------
        wins_per_venue,
        x="Win%",
        y="City",
        orientation="h",
        text="Text"      
    )
    bar_graph4.update_layout(
        title={"text":"Winpercentage in each Venue 2021 - 2026","x":0.5},
        xaxis_title="Win%",
        yaxis_title="Venues",
    paper_bgcolor="#6EADBC",
    plot_bgcolor="#6EADBC",
    showlegend=False,
    xaxis=dict(showgrid=False,zeroline=False),
    yaxis=dict(showgrid=False,zeroline=False),
    barcornerradius="25%",
    width=1300
    )
    bar_graph4.update_traces(
        width=0.7,
        marker_color="#2E7D32",
        textposition="outside"
        )      
    bar_graph4=bar_graph4.to_html(full_html=False)          
    match_data=match_data.to_dict(orient="records")
    players_info=players_info.to_dict(orient="records") 
    return render_template("dashboard.html",matches=match_data,players=players_info,batter=batter,bowler=bowler,opponents=opponents,bar_graph=bar_graph,bar_graph2=bar_graph2,pie_chart=pie_chart,bar_graph3=bar_graph3,
        bar_graph4=bar_graph4,top_batter=top_batter,top_bowler=top_bowler,top_all_rounder=top_all_rounder,graph_runs=graph_runs,graph_wickets=graph_wickets,top_10_batters=top_10_batters,top_10_bowlers=top_10_bowlers)
@app.route("/about")
def about():
    return render_template("about.html")
if __name__ == "__main__":
    app.run()    