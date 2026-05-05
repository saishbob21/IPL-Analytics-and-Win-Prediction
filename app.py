import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page config
st.set_page_config(page_title="IPL Analytics Dashboard", layout="wide")
sns.set_style("whitegrid")

st.title("🏏 IPL Performance Analytics Dashboard")

# Load dataset
df = pd.read_csv("data/ball_by_ball_ipl.csv")

# Cleaning
df = df.drop(columns=["Unnamed: 0"])
df["Date"] = pd.to_datetime(df["Date"])
df["Year"] = df["Date"].dt.year

# =========================
# SIDEBAR FILTERS
# =========================
st.sidebar.header("🔎 Filters")

teams = sorted(df["Bat First"].dropna().unique())
selected_team = st.sidebar.selectbox("Select Team", ["All"] + teams)

venues = sorted(df["Venue"].dropna().unique())
selected_venue = st.sidebar.selectbox("Select Venue", ["All"] + venues)

batters = set(df["Batter"].dropna().unique())
bowlers = set(df["Bowler"].dropna().unique())

all_players = sorted(batters.union(bowlers))

selected_player = st.sidebar.selectbox("Search Player", ["All"] + all_players)

# Apply filters
filtered_df = df.copy()

if selected_team != "All":
    filtered_df = filtered_df[
        (filtered_df["Bat First"] == selected_team) |
        (filtered_df["Bat Second"] == selected_team)
    ]

if selected_venue != "All":
    filtered_df = filtered_df[filtered_df["Venue"] == selected_venue]

if selected_player != "All":
    filtered_df = filtered_df[
        (filtered_df["Batter"] == selected_player) |
        (filtered_df["Bowler"] == selected_player)
    ]

# =========================
# KPI CARDS
# =========================
st.subheader("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

total_runs = filtered_df["Runs From Ball"].sum()
total_matches = filtered_df["Match ID"].nunique()
total_wickets = filtered_df["Wicket"].sum()
chase_success = filtered_df.groupby("Match ID")["Chased Successfully"].max().mean() * 100

col1.metric("Total Runs", int(total_runs))
col2.metric("Matches", total_matches)
col3.metric("Wickets", int(total_wickets))
col4.metric("Chase Success %", f"{chase_success:.2f}%")

# =========================
# TABS
# =========================
tab1, tab2, tab3 = st.tabs(["🏏 Batting", "🎯 Bowling", "📊 Team Analysis"])

# =========================
# BATTING TAB
# =========================
with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Batsmen")
        top_batsmen = filtered_df.groupby("Batter")["Batter Runs"].sum().sort_values(ascending=False).head(10)

        fig, ax = plt.subplots()
        sns.barplot(x=top_batsmen.values, y=top_batsmen.index, ax=ax)
        st.pyplot(fig)

    with col2:
        st.subheader("Strike Rate vs Runs")

        batsman_runs = filtered_df.groupby("Batter")["Batter Runs"].sum()
        balls = filtered_df.groupby("Batter")["Valid Ball"].sum()

        stats = pd.concat([batsman_runs, balls], axis=1)
        stats.columns = ["Runs", "Balls"]
        stats["Strike Rate"] = (stats["Runs"] / stats["Balls"]) * 100

        fig, ax = plt.subplots()
        sns.scatterplot(data=stats, x="Runs", y="Strike Rate", ax=ax)
        st.pyplot(fig)

# =========================
# BOWLING TAB
# =========================
with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Top 10 Bowlers")
        top_bowlers = filtered_df[filtered_df["Wicket"] == 1].groupby("Bowler").size().sort_values(ascending=False).head(10)

        fig, ax = plt.subplots()
        sns.barplot(x=top_bowlers.values, y=top_bowlers.index, ax=ax)
        st.pyplot(fig)

    with col2:
        st.subheader("Economy vs Wickets")

        runs_conceded = filtered_df.groupby("Bowler")["Bowler Runs Conceded"].sum()
        balls = filtered_df.groupby("Bowler")["Valid Ball"].sum()

        bowling_stats = pd.concat([runs_conceded, balls], axis=1)
        bowling_stats.columns = ["Runs", "Balls"]
        bowling_stats["Overs"] = bowling_stats["Balls"] / 6
        bowling_stats["Economy"] = bowling_stats["Runs"] / bowling_stats["Overs"]

        wickets = filtered_df[filtered_df["Wicket"] == 1].groupby("Bowler").size()
        bowling_stats = bowling_stats.join(wickets.rename("Wickets"), how="left").fillna(0)

        fig, ax = plt.subplots()
        sns.scatterplot(data=bowling_stats, x="Wickets", y="Economy", ax=ax)
        st.pyplot(fig)

# =========================
# TEAM ANALYSIS TAB
# =========================
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Most Successful Teams")
        team_wins = filtered_df.groupby("Winner")["Match ID"].nunique().sort_values(ascending=False)

        fig, ax = plt.subplots()
        sns.barplot(x=team_wins.values, y=team_wins.index, ax=ax)
        st.pyplot(fig)

    with col2:
        st.subheader("Matches per Venue")
        venue_matches = filtered_df.groupby("Venue")["Match ID"].nunique().sort_values(ascending=False).head(10)

        fig, ax = plt.subplots()
        sns.barplot(x=venue_matches.values, y=venue_matches.index, ax=ax)
        st.pyplot(fig)

    st.subheader("Season Trend")
    season_runs = filtered_df.groupby("Year")["Runs From Ball"].sum()

    fig, ax = plt.subplots()
    sns.lineplot(x=season_runs.index, y=season_runs.values, marker="o", ax=ax)
    st.pyplot(fig)

# =========================
# PLAYER ANALYSIS
# =========================
if selected_player != "All":
    st.subheader(f"📈 Performance of {selected_player}")

    is_batter = selected_player in batters
    is_bowler = selected_player in bowlers

    col1, col2 = st.columns(2)

    # ================= BATSMAN STATS =================
    if is_batter:
        with col1:
            st.markdown("### 🏏 Batting Stats")

            batter_df = df[df["Batter"] == selected_player]

            runs = batter_df["Batter Runs"].sum()
            balls = batter_df["Valid Ball"].sum()
            strike_rate = (runs / balls) * 100 if balls > 0 else 0

            fours = batter_df[batter_df["Batter Runs"] == 4].shape[0]
            sixes = batter_df[batter_df["Batter Runs"] == 6].shape[0]

            st.metric("Runs", int(runs))
            st.metric("Balls", int(balls))
            st.metric("Strike Rate", f"{strike_rate:.2f}")
            st.metric("Fours", fours)
            st.metric("Sixes", sixes)

    # ================= BOWLER STATS =================
    if is_bowler:
        with col2:
            st.markdown("### 🎯 Bowling Stats")

            bowler_df = df[df["Bowler"] == selected_player]

            runs_conceded = bowler_df["Bowler Runs Conceded"].sum()
            balls = bowler_df["Valid Ball"].sum()
            overs = balls / 6 if balls > 0 else 0
            economy = runs_conceded / overs if overs > 0 else 0

            wickets = bowler_df["Wicket"].sum()
            dot_balls = bowler_df[bowler_df["Runs From Ball"] == 0].shape[0]
            dot_pct = (dot_balls / balls) * 100 if balls > 0 else 0

            st.metric("Wickets", int(wickets))
            st.metric("Economy", f"{economy:.2f}")
            st.metric("Dot Ball %", f"{dot_pct:.2f}")

# =========================
# PLAYER COMPARISON
# =========================
st.subheader("⚔️ Player Comparison")

player_list = sorted(df["Batter"].dropna().unique())

player1 = st.selectbox("Select Player 1", player_list, index=0)
player2 = st.selectbox("Select Player 2", player_list, index=1)

batsman_runs = df.groupby("Batter")["Batter Runs"].sum()
balls = df.groupby("Batter")["Valid Ball"].sum()

batting_stats = pd.concat([batsman_runs, balls], axis=1)
batting_stats.columns = ["Runs", "Balls"]
batting_stats["Strike Rate"] = (batting_stats["Runs"] / batting_stats["Balls"]) * 100

comparison = batting_stats.loc[[player1, player2]]

st.dataframe(comparison)

fig, ax = plt.subplots()
comparison[["Runs", "Strike Rate"]].plot(kind="bar", ax=ax)
plt.xticks(rotation=0)
st.pyplot(fig)

# =========================
# WIN PREDICTION (FINAL CLEAN VERSION)
# =========================

st.subheader("🏆 Match Win Prediction (XGBoost)")

# Load dataset
ml_df = pd.read_csv("data/ipl_matches.csv")

# RAW COPY (IMPORTANT)
ml_df_raw = ml_df.copy()

# Select columns
ml_df = ml_df[[
    "team1", "team2",
    "toss_winner", "toss_decision",
    "venue", "winner"
]].dropna()

ml_df_raw = ml_df_raw[[
    "team1", "team2",
    "toss_winner", "toss_decision",
    "venue", "winner"
]].dropna()

# =========================
# FEATURE ENGINEERING
# =========================

# Team strength
team_win_rate = ml_df_raw.groupby("team1")["winner"].apply(
    lambda x: (x == x.name).mean()
)

ml_df["team1_strength"] = ml_df["team1"].map(team_win_rate)
ml_df["team2_strength"] = ml_df["team2"].map(team_win_rate)

# Toss advantage
ml_df["toss_advantage"] = (ml_df["toss_winner"] == ml_df["team1"]).astype(int)

# Head-to-head
def get_h2h(row):
    t1 = row["team1"]
    t2 = row["team2"]

    matches = ml_df_raw[
        ((ml_df_raw["team1"] == t1) & (ml_df_raw["team2"] == t2)) |
        ((ml_df_raw["team1"] == t2) & (ml_df_raw["team2"] == t1))
    ]

    if len(matches) == 0:
        return 0.5

    wins = (matches["winner"] == t1).sum()
    return wins / len(matches)

ml_df["h2h_team1"] = ml_df.apply(get_h2h, axis=1)

# Venue strength
def get_venue_strength(row):
    team = row["team1"]
    venue = row["venue"]

    matches = ml_df_raw[ml_df_raw["venue"] == venue]

    if len(matches) == 0:
        return 0.5

    wins = (matches["winner"] == team).sum()
    return wins / len(matches)

ml_df["venue_team1_strength"] = ml_df.apply(get_venue_strength, axis=1)

# =========================
# ENCODING
# =========================
from sklearn.preprocessing import LabelEncoder

team_encoder = LabelEncoder()
venue_encoder = LabelEncoder()
toss_encoder = LabelEncoder()
winner_encoder = LabelEncoder()

ml_df["team1"] = team_encoder.fit_transform(ml_df["team1"])
ml_df["team2"] = team_encoder.transform(ml_df["team2"])
ml_df["toss_winner"] = team_encoder.transform(ml_df["toss_winner"])

ml_df["toss_decision"] = toss_encoder.fit_transform(ml_df["toss_decision"])
ml_df["venue"] = venue_encoder.fit_transform(ml_df["venue"])
ml_df["winner"] = winner_encoder.fit_transform(ml_df["winner"])

# =========================
# MODEL TRAINING
# =========================
from sklearn.model_selection import train_test_split, cross_val_score
from xgboost import XGBClassifier

X = ml_df[[
    "team1", "team2",
    "toss_winner", "toss_decision",
    "venue",
    "team1_strength", "team2_strength",
    "toss_advantage",
    "h2h_team1",
    "venue_team1_strength"
]]

y = ml_df["winner"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = XGBClassifier(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    eval_metric='mlogloss'
)

model.fit(X_train, y_train)

# Accuracy
accuracy = model.score(X_test, y_test)
st.write(f"Model Accuracy: {accuracy*100:.2f}%")

# Cross-validation
cv_scores = cross_val_score(model, X, y, cv=5)
st.write(f"Cross Validation Accuracy: {cv_scores.mean()*100:.2f}%")

# =========================
# PREDICTION UI
# =========================

st.markdown("### 🏏 Predict Match Winner")

team_list = list(team_encoder.classes_)
venue_list = list(venue_encoder.classes_)
toss_list = list(toss_encoder.classes_)

col1, col2 = st.columns(2)

with col1:
    team1 = st.selectbox("Team 1", team_list)
    toss_winner = st.selectbox("Toss Winner", team_list)
    venue = st.selectbox("Venue", venue_list)

with col2:
    team2 = st.selectbox("Team 2", team_list)
    toss_decision = st.selectbox("Toss Decision", toss_list)

# =========================
# BUTTON + PREDICTION
# =========================

if st.button("Predict Winner"):

    # Team strength (RAW)
    team1_strength = (
        (ml_df_raw["winner"] == team1).sum() /
        ((ml_df_raw["team1"] == team1) | (ml_df_raw["team2"] == team1)).sum()
    )

    team2_strength = (
        (ml_df_raw["winner"] == team2).sum() /
        ((ml_df_raw["team1"] == team2) | (ml_df_raw["team2"] == team2)).sum()
    )

    # Toss advantage
    toss_advantage = 1 if toss_winner == team1 else 0

    # Head-to-head
    h2h_matches = ml_df_raw[
        ((ml_df_raw["team1"] == team1) & (ml_df_raw["team2"] == team2)) |
        ((ml_df_raw["team1"] == team2) & (ml_df_raw["team2"] == team1))
    ]

    if len(h2h_matches) == 0:
        h2h_team1 = 0.5
    else:
        wins = (h2h_matches["winner"] == team1).sum()
        h2h_team1 = wins / len(h2h_matches)

    # Venue strength
    venue_matches = ml_df_raw[ml_df_raw["venue"] == venue]

    if len(venue_matches) == 0:
        venue_team1_strength = 0.5
    else:
        wins = (venue_matches["winner"] == team1).sum()
        venue_team1_strength = wins / len(venue_matches)

    # Input
    input_data = pd.DataFrame([[
        team_encoder.transform([team1])[0],
        team_encoder.transform([team2])[0],
        team_encoder.transform([toss_winner])[0],
        toss_encoder.transform([toss_decision])[0],
        venue_encoder.transform([venue])[0],
        team1_strength,
        team2_strength,
        toss_advantage,
        h2h_team1,
        venue_team1_strength
    ]], columns=X.columns)

    # Prediction
    prediction = model.predict(input_data)[0]
    winner = winner_encoder.inverse_transform([prediction])[0]

    st.success(f"🏆 Predicted Winner: {winner}")

    # Insights
    st.markdown("### 📊 Match Insights")

    c1, c2, c3 = st.columns(3)
    c1.metric("Team Strength", f"{team1_strength:.2f}")
    c2.metric("Head-to-Head %", f"{h2h_team1*100:.1f}%")
    c3.metric("Venue Win %", f"{venue_team1_strength*100:.1f}%")

# =========================
# FOOTER
# =========================
st.markdown("---")
st.markdown("Developed by Saish Bobhate")