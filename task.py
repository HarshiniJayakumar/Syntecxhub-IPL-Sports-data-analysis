import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")
matches = pd.read_csv("matches.csv")
deliveries = pd.read_csv("deliveries.csv")
top_runs = deliveries.groupby("batter")["batsman_runs"].sum().sort_values(ascending=False)
balls = deliveries.groupby("batter").size()
strike_rate = ((top_runs / balls) * 100).sort_values(ascending=False)
played = pd.concat([matches["team1"], matches["team2"]]).value_counts()
won = matches["winner"].value_counts()
win_rate = ((won / played) * 100).sort_values(ascending=False)
season_data = deliveries.merge(matches[["id", "season"]],left_on="match_id",right_on="id")

season_runs = season_data.groupby("season")["batsman_runs"].sum()

player1 = input("Enter First Player Name: ").strip()
player2 = input("Enter Second Player Name: ").strip()
players = [player1, player2]
player_data = season_data[season_data["batter"].isin(players)]

comparison = player_data.groupby(
    ["season", "batter"])["batsman_runs"].sum().unstack(fill_value=0)
if comparison.empty:
    print("Player name not found. Please enter valid player names.")


top_runs.head(10).plot(kind="bar", figsize=(9,5), color="royalblue")
plt.title("Top 10 Run Scorers")
plt.ylabel("Runs")
plt.tight_layout()
plt.savefig("Top_Run_Scorers.png")
plt.show()

win_rate.plot(kind="bar", figsize=(9,5), color="green")
plt.title("Team Win Rate")
plt.ylabel("Win %")
plt.tight_layout()
plt.savefig("Team_Win_Rate.png")
plt.show()

season_runs.plot(marker="o", figsize=(9,5), color="red")
plt.title("Runs Per Season")
plt.ylabel("Runs")
plt.tight_layout()
plt.savefig("Runs_Per_Season.png")
plt.show()

top_runs.head(10).plot(kind="bar", figsize=(9,5), color="orange")
plt.title("Top 10 Players by Total Runs")
plt.ylabel("Runs")
plt.tight_layout()
plt.savefig("Top_10_Player_Runs.png")
plt.show()

comparison.plot(marker="o", figsize=(9,5))
plt.title("Player Performance Across Seasons")
plt.xlabel("Season")
plt.ylabel("Runs")
plt.tight_layout()
plt.savefig("Player_Comparison.png")
plt.show()

top_runs.to_frame("Runs").to_csv("Top_Scorers.csv", index=True)
strike_rate.to_frame("Strike Rate").to_csv("Strike_Rate.csv", index=True)
win_rate.to_frame("Win Rate (%)").to_csv("Team_Win_Rate.csv", index=True)
season_runs.to_frame("Season Runs").to_csv("Season_Runs.csv", index=True)
comparison.to_csv("Player_Comparison.csv", index=True)

with open("IPL_Insights.txt", "w") as f:
    f.write("IPL SPORTS DATA ANALYSIS\n")
    f.write("="*35 + "\n\n")
    f.write(f"Top Run Scorer: {top_runs.idxmax()} ({top_runs.max()} Runs)\n")
    f.write(f"Highest Strike Rate: {strike_rate.idxmax()} ({strike_rate.max():.2f})\n")
    f.write(f"Best Team: {win_rate.idxmax()} ({win_rate.max():.2f}% Win Rate)\n")
    f.write(f"Highest Scoring Season: {season_runs.idxmax()} ({season_runs.max()} Runs)\n")
    f.write(f"Compared Players: {player1} vs {player2}\n")

print("\n=== ANALYSIS COMPLETED ===")
