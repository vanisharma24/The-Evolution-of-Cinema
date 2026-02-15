import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
df = pd.read_csv('imdb_movies.csv')  # Your filename
df['decade'] = (df['year'] // 10) * 10

print("✅ Data loaded successfully!")
print(f"Total movies: {len(df)}")

# ============================================
# VISUALIZATION 1: Ratings by Decade
# ============================================
decade_ratings = df.groupby('decade')['rating'].mean().reset_index()

plt.figure(figsize=(12, 6))
plt.plot(decade_ratings['decade'], decade_ratings['rating'], 
         marker='o', linewidth=2.5, markersize=8, color='#2C4563')

plt.title('Average Movie Rating by Decade (1940-2024)', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Decade', fontsize=12)
plt.ylabel('Average Rating', fontsize=12)
plt.grid(True, alpha=0.3)
plt.ylim(df['rating'].min() - 0.5, df['rating'].max() + 0.5)

for i, row in decade_ratings.iterrows():
    plt.text(row['decade'], row['rating'] + 0.05, 
             f"{row['rating']:.2f}", ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('ratings_by_decade.png', dpi=300, bbox_inches='tight')
plt.close()  # Close instead of show
print("✅ Saved: ratings_by_decade.png")

# ============================================
# VISUALIZATION 2: Revenue vs Rating
# ============================================
df_revenue = df.dropna(subset=['gross_millions'])

plt.figure(figsize=(12, 7))
scatter = plt.scatter(df_revenue['rating'], df_revenue['gross_millions'], 
                     alpha=0.6, s=60, c=df_revenue['year'], cmap='viridis')

plt.title('Box Office Revenue vs Movie Rating', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('IMDB Rating', fontsize=12)
plt.ylabel('Box Office Revenue (Millions $)', fontsize=12)
plt.grid(True, alpha=0.3)

cbar = plt.colorbar(scatter)
cbar.set_label('Year', fontsize=11)

z = np.polyfit(df_revenue['rating'], df_revenue['gross_millions'], 1)
p = np.poly1d(z)
plt.plot(df_revenue['rating'], p(df_revenue['rating']), 
         "r--", alpha=0.8, linewidth=2, label='Trend')

plt.legend()
plt.tight_layout()
plt.savefig('revenue_vs_rating.png', dpi=300, bbox_inches='tight')
plt.close()  # Close instead of show
print("✅ Saved: revenue_vs_rating.png")

correlation = df_revenue['rating'].corr(df_revenue['gross_millions'])
print(f"\n💰 Correlation between Rating and Revenue: {correlation:.3f}")

# ============================================
# VISUALIZATION 3: Top Genres by Decade
# ============================================

# Extract primary genre (first one listed)
df['primary_genre'] = df['genre'].str.split(',').str[0].str.strip()

# Get top 5 genres overall
top_genres = df['primary_genre'].value_counts().head(5).index

# Filter for top genres
df_top_genres = df[df['primary_genre'].isin(top_genres)]

# Count movies per genre per decade
genre_decade = df_top_genres.groupby(['decade', 'primary_genre']).size().reset_index(name='count')

# Create stacked area chart
pivot_data = genre_decade.pivot(index='decade', columns='primary_genre', values='count').fillna(0)

plt.figure(figsize=(14, 7))
pivot_data.plot(kind='area', stacked=True, alpha=0.7, figsize=(14, 7), 
                colormap='Set2', linewidth=2)

plt.title('Genre Evolution Across Decades (1940-2024)', 
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Decade', fontsize=12)
plt.ylabel('Number of Movies', fontsize=12)
plt.legend(title='Genre', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig('genre_evolution.png', dpi=300, bbox_inches='tight')
plt.close()
print("✅ Saved: genre_evolution.png")

print("\n🎬 Top 5 Genres:")
print(df['primary_genre'].value_counts().head(5))