from cProfile import label
import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import ast 
st.markdown("""<style>.stApp {background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); ;} .blockcontainer{background: rgba(0,0,0,0.3); padding: 2rem; border-radius: 15px;}</style>""", unsafe_allow_html=True)
def neon_metric(label, value):
    st.markdown(f"""<div style ="background:rgba(0,0,0,0.4); padding: 15px; border-radius: 12px; box-shadow: 0 0 10px #00F5D4; text-align: center; "><h4 style="color: #aaa;">{label}</h4><h2 style="color: #00F5D4;">{value}</h2></div>""", unsafe_allow_html=True)           
st.markdown("""<style>footer{visibility: hidden;}</style>""", unsafe_allow_html=True)
st.set_page_config(page_title="🎧 United States Top 50 Playlist Analytics Dashboard", layout="wide")
# Set the title of the app
st.title("United States Top 50 Playlist Performance and Song Popularity Trend Analysis Dashboard")
# Load the dataset
url ="https://github.com/siya2799/US-top50-playlist-analysis/blob/main/data/Atlantic_United_States.csv"
df=pd.read_csv(url)
#Convert the 'Date' column to datetime format
df['date'] = pd.to_datetime(df['date'])
#Create "primary artist" column by extracting the first artist from the 'artist' column
df['artist'] = df['artist'].str.lower().str.strip()
df['primary_artist'] = df['artist'].str.replace(r'\(.*?\)', '', regex=True)
df['primary_artist'] = df['primary_artist'].str.replace( r'\b(feat|ft|featuring)\b\.?.*', '', regex=True)
df['primary_artist'] = df['primary_artist'].str.replace(r'\s+', ' ', regex=True).str.strip()
#create "song_id" column by combining "song" and "artist"
df['song_id'] = df['song'].str.lower().str.strip() + "_" + df['primary_artist'].str.lower().str.strip()
#Sidebar filters
st.sidebar.title("🎛️ Filters")
#Date Range
min_date = df['date'].min()
max_date = df['date'].max()
date_range = st.sidebar.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
#Artist Filter
artists = st.sidebar.multiselect("Artist", df['primary_artist'].dropna().unique())
#Rank Slider 
rank_range = st.sidebar.slider("Rank Range", 1, 50, (1, 50))
#Album type
album_type = st.sidebar.multiselect("Album Type", df['album_type'].unique())
#Apply filters to the dataset
filtered_df = df.copy()
if len(date_range) == 2:
    filtered_df = filtered_df[(filtered_df['date'] >= pd.to_datetime(date_range[0])) & (filtered_df['date'] <= pd.to_datetime(date_range[1]))]
if artists:
    filtered_df = filtered_df[filtered_df['primary_artist'].isin(artists)]
filtered_df = filtered_df[(filtered_df['position'] >= rank_range[0]) & (filtered_df['position'] <= rank_range[1])]
if album_type:
    filtered_df = filtered_df[filtered_df['album_type'].isin(album_type)] 
#Current top 10 songs for dynamic default selection
st.subheader("🔥 Top 10 Songs Right Now")
latest_date = filtered_df['date'].max()
top_songs = filtered_df[filtered_df['date'] == latest_date].sort_values('position').head(10)
rows=(top_songs.iloc[i:i+5] for i in range(0, len(top_songs), 5))
for row in rows:
    cols = st.columns(len(row))
    for i, (_, song) in enumerate(row.iterrows()):
        with cols[i]:
            img = song.get('album_image_url', None)
            image_url = img
            default_img= "https://upload.wikimedia.org/wikipedia/en/7/7b/Spotify_logo_without_text.svg" 
            if isinstance(img, str) and img.startswith("http"):
                image_url = img 
            else:
                image_url = default_img
            st.markdown(f"""<div style="background: rgba(0,0,0,0.5);padding: 10px;border-radius: 12px;text-align: center;box-shadow: 0 0 10px #00F5D4;margin: 10px;"><img src="{image_url}" style="width:100%; border-radius:10px;" /><p style="margin-top:8px;font-size:14px;font-weight:bold; color:white;"> #{int(song['position'])} {song['song']}</p><p style="font-size:12px;color:#aaaaaa;">{song['primary_artist']}</p></div>""", unsafe_allow_html=True)      
#KPI calculations
songs_on_playlist = filtered_df['song_id'].nunique()
song_group = filtered_df.groupby('song_id')
analysis_df = pd.DataFrame({
    'days_on_chart': song_group['date'].nunique(),
    'average_rank': song_group['position'].mean(),
    'best_rank': song_group['position'].min(),
    'rank_volatility': song_group['position'].std(),
    'popularity': song_group['popularity'].mean(),
    'duration_mins': song_group['duration_ms'].mean() / 60000,})
analysis_df = analysis_df.reset_index()
#Popularity Trend 
filtered_df=filtered_df.sort_values(['song_id','date'])
filtered_df['popularity_trend'] = filtered_df.groupby('song_id')['popularity'].rolling(window=7, min_periods=1).mean().reset_index(level=0, drop=True)
latest_popularity = filtered_df.groupby('song_id').tail(1)[['song_id', 'popularity_trend']]
analysis_df = analysis_df.merge(latest_popularity, on='song_id', how='left')
#Artist Dominance
artist_days = filtered_df.groupby('primary_artist')['date'].nunique()
artist_songs = filtered_df.groupby('primary_artist')['song_id'].nunique()
artist_df = pd.DataFrame({'days_on_playlist': artist_days, 'unique_songs': artist_songs}).reset_index()
artist_avg_rank = filtered_df.groupby('primary_artist')['position'].mean().reset_index(name='artist_avg_rank')
global_artist_df = df.groupby('primary_artist').agg({'song_id': 'nunique', 'date': 'nunique', 'position': 'mean'}).reset_index()
global_artist_df.columns = ['primary_artist', 'unique_songs', 'days_on_playlist', 'artist_avg_rank']
global_artist_df['dominance_raw_global'] = global_artist_df['unique_songs'] * global_artist_df['days_on_playlist'] / (global_artist_df['artist_avg_rank'])
global_max=global_artist_df['dominance_raw_global'].max()
artist_df=artist_df.merge(artist_avg_rank, on='primary_artist', how='left')
artist_df['dominance_raw'] = artist_df['unique_songs'] * artist_df['days_on_playlist'] / (artist_df['artist_avg_rank'])
artist_df['dominance'] = (artist_df['dominance_raw'] / global_max) * 100 
analysis_df = analysis_df.merge(artist_df[['primary_artist', 'dominance']], left_on='song_id', right_on='primary_artist', how='left')
#explicit share
explicit_share = filtered_df['is_explicit'].dropna().mean()
#Display KPIs
st.subheader("Key Performance Indicators (KPIs)")
col1, col2, col3, col4 = st.columns(4)
with col1:
    neon_metric("Average Days on chart", round(analysis_df['days_on_chart'].mean(), 1))
with col2:
    neon_metric("Average Rank", round(analysis_df['average_rank'].mean(), 2))
with col3:
    neon_metric("Best Rank (Avg)", round(analysis_df['best_rank'].mean(), 2))
with col4:
    neon_metric("Rank Volatility", round(analysis_df['rank_volatility'].mean(), 2))
col5, col6, col7= st.columns(3)
with col5:
    neon_metric("Popularity Trend", round(analysis_df['popularity_trend'].mean(), 2))
with col6:
    neon_metric("Artist Dominance", f"{round(artist_df['dominance'].max(), 1)}%")
with col7:
    neon_metric("Explicit Share", f"{explicit_share:.1%}")
#Tabs layout
tab1, tab2, tab3, tab4 = st.tabs(["📈 Ranking Trends", "🎤 Artist Insights", "📊 Popularity Analysis", "🎵 Content Analysis"])
#Tab 1: Ranking Trends
with tab1:
    st.subheader("Song Rank Trends")
    sample_songs = filtered_df['song_id'].drop_duplicates().head(10)
    fig=px.line(filtered_df[filtered_df['song_id'].isin(sample_songs)], x='date', y='position', color='song_id', markers=True, title='Rank Trajectories of Sample Songs' , hover_data=['song_id', 'primary_artist', 'position'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', legend_title_text='Song ID', legend=dict(font=dict(color='white'), yanchor='top', y=1, xanchor='left', x=1.02), xaxis_title='Date', yaxis_title='Rank')
    fig.update_traces(line=dict(width=2), marker=dict(size=6))
    fig.update_yaxes(autorange='reversed')
    st.plotly_chart(fig, use_container_width=True)
#Tab 2: Artist Insights
with tab2:
    st.subheader("🎤 Artist Showcase")
    top_artist_for_cover = artist_df.sort_values('dominance', ascending=False).head(3)
    for _, artist_row in top_artist_for_cover.iterrows():
         artist = artist_row['primary_artist']
         dominance = artist_row['dominance']
         st.markdown(f"""<h3 style="color: #00F5D4;">  🔥 {artist.title()}({round(dominance, 1)}%) </h3> """, unsafe_allow_html=True)
    st.subheader("Artist Dominance Leaderboard")
    top_artists = artist_df.sort_values('dominance', ascending=False).head(10)
    fig=px.bar(top_artists, x='dominance', y='primary_artist', orientation='h', title='Top Artists by Dominance', text='dominance', color='dominance', color_continuous_scale='turbo', hover_data=['primary_artist', 'days_on_playlist', 'unique_songs'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title='Dominance Score', yaxis_title='Artist', font=dict(color='white'), yaxis=dict(autorange='reversed'), legend=dict(font=dict(color='white'), yanchor='top', y=1, xanchor='left', x=1.02))
    st.plotly_chart(fig, use_container_width=True)
#Tab 3: Popularity Analysis
with tab3:
    st.subheader("Popularity vs Rank Analysis")
    fig=px.scatter(analysis_df, x='popularity_trend', y='average_rank', title='Popularity vs Rank Analysis', trendline='ols',color='popularity_trend',size='popularity_trend', hover_data=['song_id', 'primary_artist', 'popularity_trend'])
    fig.update_yaxes(autorange='reversed')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title='Popularity Trend', yaxis_title='Average Rank', font=dict(color='white'), legend=dict(font=dict(color='white'), yanchor='top', y=1, xanchor='left', x=1.02))
    st.plotly_chart(fig, use_container_width=True)
#Tab 4: Content Analysis
with tab4:
    st.subheader("Explicit vs Non-explicit Performance")
    fig=px.box(filtered_df, x='is_explicit', y='position', title='Explicit vs Non-Explicit Rank Distribution', color='is_explicit', hover_data=['song_id', 'primary_artist'], color_discrete_map={True: 'red', False: 'green'})
    fig.update_yaxes(autorange='reversed')
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title='Explicit', yaxis_title='Rank', font=dict(color='white'), legend=dict(font=dict(color='white'), yanchor='top', y=1, xanchor='left', x=1.02))
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("Duration vs Popularity Trend Analysis")
    fig=px.scatter(analysis_df, x='duration_mins', y='popularity_trend', title='Duration vs Popularity Trend', trendline='ols', color='popularity_trend', size='popularity_trend', hover_data=['song_id', 'primary_artist', 'duration_mins'])
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', xaxis_title='Duration (minutes)', yaxis_title='Popularity Trend', font=dict(color='white'), legend=dict(font=dict(color='white'), yanchor='top', y=1, xanchor='left', x=1.02))
    st.plotly_chart(fig, use_container_width=True)