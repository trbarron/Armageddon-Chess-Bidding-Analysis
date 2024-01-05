import psycopg2

# Function to connect to the PostgreSQL database
def connect_to_db():
    return psycopg2.connect(
        dbname="chessDB",
        user="postgres",
        host="localhost",
        password="admin",
        port="5432"
    )

# SQL query to create the statistics table
create_table_query = """
CREATE TABLE IF NOT EXISTS fen_statistics (
    id SERIAL PRIMARY KEY,
    fen TEXT NOT NULL,
    time_control TEXT NOT NULL,
    min_elo INT,
    max_elo INT,
    median_elo INT,
    mode_elo INT,
    q1_elo INT,
    q3_elo INT,
    std_dev_elo FLOAT,
    count INT
);
"""

# SQL query to calculate and insert statistics
insert_stats_query = """
INSERT INTO fen_statistics (fen, time_control, min_elo, max_elo, median_elo, mode_elo, q1_elo, q3_elo, std_dev_elo, count)
SELECT 
    fen_curr,
    time_control,
    MIN(elo),
    MAX(elo),
    PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY elo) AS median_elo,
    MODE() WITHIN GROUP (ORDER BY elo) AS mode_elo,
    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY elo) AS q1_elo,
    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY elo) AS q3_elo,
    STDDEV(elo),
    COUNT(*)
FROM 
    moves_compared_to_elo
GROUP BY 
    fen_curr, time_control;
"""

# Connect to the database and execute the queries
conn = connect_to_db()
cursor = conn.cursor()

# Create the new table
cursor.execute(create_table_query)

# Calculate and insert the statistics
cursor.execute(insert_stats_query)

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()
