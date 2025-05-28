import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")
st.title("🏀 LeBron James Career Statistics Dashboard")

# Load main stats file
df = pd.read_csv('lebron_stats.csv')
summary_df = pd.read_csv('summary.csv')
perteam_df = pd.read_csv('perteam.csv')

stat_name_map = {
    'G': 'Games Played',
    'GS': 'Games Started',
    'MP': 'Minutes Played',
    'FG': 'Field Goals Made',
    'FGA': 'Field Goal Attempts',
    'FG%': 'Field Goal %',
    '3P': '3-Pointers Made',
    '3PA': '3-Point Attempts',
    '3P%': '3-Point %',
    '2P': '2-Pointers Made',
    '2PA': '2-Point Attempts',
    '2P%': '2-Point %',
    'eFG%': 'Effective FG %',
    'FT': 'Free Throws Made',
    'FTA': 'Free Throw Attempts',
    'FT%': 'Free Throw %',
    'ORB': 'Offensive Rebounds',
    'DRB': 'Defensive Rebounds',
    'TRB': 'Total Rebounds',
    'AST': 'Assists',
    'STL': 'Steals',
    'BLK': 'Blocks',
    'TOV': 'Turnovers',
    'PF': 'Personal Fouls',
    'PTS': 'Points',
    'Trp-Dbl': 'Triple-Doubles'
}


# === SECTION 1: Default LeBron Stats Visualizations === #
st.header("📊 Overall Per-Regular Season Stats")

# Show full table
st.dataframe(df)

# Set 'Season' as index
df.set_index('Season', inplace=True)

# Field Goals Per Game
st.subheader("Field Goals Per Game Over Seasons")
st.line_chart(df['FG'])

# Assists and Rebounds
st.subheader("Assists and Rebounds Per Game Over Seasons")
st.line_chart(df[['AST', 'TRB']])

# Reset index for further use
df.reset_index(inplace=True)

# # Multiselect for custom stat visualization
# st.subheader("Select Statistics to Visualize")
# stats_options = ['G','GS','MP','FG','FGA','FG%','3P','3PA','3P%','2P','2PA','2P%','eFG%','FT','FTA','FT%','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','Trp-Dbl']
# selected_stats = st.multiselect("Choose statistics:", stats_options, default=['FG'])

# Reverse map to get original stat names from labels
reverse_stat_map = {v: k for k, v in stat_name_map.items()}

selected_labels = st.multiselect("Select Statistics to Visualize:", list(stat_name_map.values()), default=['Field Goals Made'])
selected_stats = [reverse_stat_map[label] for label in selected_labels]

if selected_stats:
    st.line_chart(df.set_index('Season')[selected_stats])

# === SECTION 2: Final Career Summary for Cumulative Stats === #
st.header("📈 LeBron James: 22-Year Career Summary")

st.subheader("🏆 All-Time Career Totals and Averages")

# Assume summary_df has a single row (22-year total)
career_row = summary_df.iloc[0]  # first and only row

# Display key stats
col1, col2, col3 = st.columns(3)
col1.metric("Total Points", f"{int(career_row['PTS']):,}")
col2.metric("Total Assists", f"{int(career_row['AST']):,}")
col3.metric("Total Rebounds", f"{int(career_row['TRB']):,}")

col4, col5, col6 = st.columns(3)
col4.metric("Games Played", f"{int(career_row['G']):,}")
col5.metric("Field Goals Made", f"{int(career_row['FG']):,}")
col6.metric("Free Throws Made", f"{int(career_row['FT']):,}")

col7, col8, col9 = st.columns(3)
col7.metric("FG%", f"{career_row['FG%']:.2f}")
col8.metric("3P%", f"{career_row['3P%']:.2f}")
col9.metric("FT%", f"{career_row['FT%']:.2f}")

# Expandable table to view all stats in raw form
with st.expander("📋 View Full Career Summary Data"):
    st.dataframe(summary_df.transpose().reset_index().rename(columns={'index': 'Statistic', 0: 'Value'}))



# === SECTION 3: Per-Team Stats as Bar Graph (Improved Labels) === #
st.header("🏟️ Per-Team Comparison")

# Ensure clean column names
perteam_df.columns = perteam_df.columns.str.strip()

# Friendly names mapping
stat_name_map = {
    'G': 'Games Played',
    'GS': 'Games Started',
    'MP': 'Minutes Played',
    'FG': 'Field Goals Made',
    'FGA': 'Field Goal Attempts',
    'FG%': 'Field Goal %',
    '3P': '3-Pointers Made',
    '3PA': '3-Point Attempts',
    '3P%': '3-Point %',
    '2P': '2-Pointers Made',
    '2PA': '2-Point Attempts',
    '2P%': '2-Point %',
    'eFG%': 'Effective FG %',
    'FT': 'Free Throws Made',
    'FTA': 'Free Throw Attempts',
    'FT%': 'Free Throw %',
    'ORB': 'Offensive Rebounds',
    'DRB': 'Defensive Rebounds',
    'TRB': 'Total Rebounds',
    'AST': 'Assists',
    'STL': 'Steals',
    'BLK': 'Blocks',
    'TOV': 'Turnovers',
    'PF': 'Personal Fouls',
    'PTS': 'Points',
    'Trp-Dbl': 'Triple-Doubles'
}

# Reverse map for lookup
reverse_stat_map = {v: k for k, v in stat_name_map.items()}

# Let user pick a stat by display name
team_bar_label = st.selectbox("Choose a stat to compare across teams:", list(stat_name_map.values()), key="team_bar_metric")
team_bar_metric = reverse_stat_map[team_bar_label]  # Get actual column name

# Plot grouped bar chart
fig3, ax3 = plt.subplots(figsize=(12, 6))
sns.barplot(data=perteam_df, x='Team', y=team_bar_metric, hue='Team', ax=ax3)
ax3.set_title(f"{team_bar_label} by Team")
ax3.set_xlabel("Teams")
ax3.set_ylabel(team_bar_label)
plt.xticks(rotation=45)
st.pyplot(fig3)

# Show full data
st.dataframe(perteam_df)


