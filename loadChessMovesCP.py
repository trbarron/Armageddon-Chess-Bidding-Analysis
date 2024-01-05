import json
import psycopg2

# Database connection parameters - replace these with your database details
db_params = {
    'database': 'chessDB',
    'user': 'postgres',
    'password': 'admin',
    'host': 'localhost',
    'port': 5432
}

# Function to parse JSON and extract required data
def parse_json(file_path):
    data_to_insert = []
    with open(file_path, 'r') as file:
        i = 0
        for line in file:
            json_line = json.loads(line)

            fen = json_line['fen']
            best_eval = None
            is_white_to_move = 'w' in fen.split(' ')[1]

            for eval in json_line['evals']:
                for pv in eval['pvs']:
                    try:
                        cp = pv['cp']
                        if best_eval is None:
                            best_eval = cp
                        elif is_white_to_move and cp > best_eval:
                            best_eval = cp
                        elif not is_white_to_move and cp < best_eval:
                            best_eval = cp
                        data_to_insert.append((fen, best_eval))
                        i += 1
                        if i % 1000000 == 0: print("completed:" + str(i))
                    except:
                        pass
    return data_to_insert

# Function to create database table
def create_table(connection):
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS evaluations (
                id SERIAL PRIMARY KEY,
                fen VARCHAR(255) NOT NULL,
                best_evaluation INT
            );
        """)
        connection.commit()

# Function to insert data into the database
def insert_data(connection, data):
    with connection.cursor() as cursor:
        insert_query = 'INSERT INTO evaluations (fen, best_evaluation) VALUES (%s, %s)'
        cursor.executemany(insert_query, data)
        connection.commit()

# Main execution
if __name__ == '__main__':
    data = parse_json('lichess_db_eval.json')

    # Connect to the database
    conn = psycopg2.connect(**db_params)

    # Create the table
    create_table(conn)

    # Insert the data
    insert_data(conn, data)

    # Close the database connection
    conn.close()
