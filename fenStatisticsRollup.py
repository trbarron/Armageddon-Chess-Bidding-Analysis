import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

def connect_to_db():
    return psycopg2.connect(
        dbname="chessDB",
        user="postgres",
        host="localhost",
        password="admin",
        port="5432"
    )

def fetch_data(cursor):
    fetch_query = """
    SELECT fen, time_control, median_elo, count
    FROM fen_statistics
    WHERE count > 20
      AND char_length(fen) - char_length(replace(fen, ' ', '')) >= 5
      AND CAST(SPLIT_PART(fen, ' ', 6) AS INTEGER) >= 5
    ORDER BY CAST(SPLIT_PART(fen, ' ', 6) AS INTEGER) DESC;
    """
    cursor.execute(fetch_query)
    return cursor.fetchall()

def analyze_data(data, min_time_controls=5):
    df = pd.DataFrame(data, columns=['fen', 'time_control', 'median_elo', 'count'])
    df['median_elo'] = pd.to_numeric(df['median_elo'], errors='coerce')
    grouped = df.groupby(['fen', 'time_control']).median_elo.mean().unstack()
    filtered_grouped = grouped[grouped.count(axis=1) >= min_time_controls]
    return filtered_grouped.reset_index()

def create_table_if_not_exists(cursor):
    create_table_query = """
    CREATE TABLE IF NOT EXISTS analyzed_fen_statistics (
        fen TEXT,
        time_control TEXT,
        average_elo REAL,
        PRIMARY KEY (fen, time_control)
    );
    """
    cursor.execute(create_table_query)

def save_data_to_db(cursor, data):
    for index, row in data.iterrows():
        fen = row['fen']
        for time_control in data.columns[1:]:
            elo = row[time_control]
            if not pd.isna(elo):
                insert_query = """
                INSERT INTO analyzed_fen_statistics (fen, time_control, average_elo)
                VALUES (%s, %s, %s)
                ON CONFLICT (fen, time_control) DO UPDATE 
                SET average_elo = EXCLUDED.average_elo;
                """
                cursor.execute(insert_query, (fen, time_control, elo))


def analyze_and_plot_data(data, min_time_controls=5, min_count=10):
    df = pd.DataFrame(data, columns=['fen', 'time_control', 'median_elo', 'count'])
    df['median_elo'] = pd.to_numeric(df['median_elo'], errors='coerce')

    # Handle non-standard time_control formats
    df[['starting_time', 'increment']] = df['time_control'].str.split('+', expand=True)
    df = df[df['starting_time'].str.isnumeric() & df['increment'].str.isnumeric()]
    df[['starting_time', 'increment']] = df[['starting_time', 'increment']].astype(int)

    # Group and aggregate data
    grouped = df.groupby(['fen', 'time_control', 'starting_time', 'increment']).agg({'median_elo': 'mean', 'count': 'sum'}).unstack(level=[1, 2, 3])
    filtered_grouped = grouped[grouped['median_elo'].count(axis=1) >= min_time_controls]

    for fen, row in filtered_grouped.iterrows():
        median_elo_row = row['median_elo'].dropna()
        count_row = row['count'].reindex(median_elo_row.index)

        # Create a DataFrame for sorting
        sort_df = median_elo_row.index.to_frame(index=False)
        sort_df['median_elo'] = median_elo_row.values
        sorted_df = sort_df.sort_values(by=['starting_time', 'increment'])

        if not sorted_df.empty:
            ax = sorted_df.plot(x='time_control', y='median_elo', kind='bar', figsize=(12, 6))
            plt.title(f"Comparative ELO Ratings for {fen}")
            plt.xlabel("Time Control")
            plt.ylabel("Average Median ELO")

            # Set x-axis labels to include count
            counts = [count_row.loc[(tc, st, inc)] for tc, st, inc in zip(sorted_df['time_control'], sorted_df['starting_time'], sorted_df['increment'])]
            ax.set_xticklabels([f"{tc} ({int(count)} instances)" for tc, count in zip(sorted_df['time_control'], counts)])

            plt.tight_layout()
            plt.show()  # Or save the plot as an image

# Main execution
conn = connect_to_db()
cursor = conn.cursor()

create_table_if_not_exists(cursor)  # Create the table if it doesn't exist

data = fetch_data(cursor)
# analyzed_data = analyze_data(data)
# save_data_to_db(cursor, analyzed_data)

analyze_and_plot_data(data)


conn.commit()
cursor.close()
conn.close()
