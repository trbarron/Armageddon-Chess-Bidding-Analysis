import chess.pgn
import psycopg2
import io

# Function to connect to the PostgreSQL database
def connect_to_db():
    try:
        return psycopg2.connect(
            dbname="chessDB",
            user="postgres",
            host="localhost",
            password="admin",
            port="5432"
        )
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

# Function to insert data into the database
def insert_data(cursor, fen_curr, fen_prev, elo, time_control):
    try:
        query = "INSERT INTO moves_compared_to_elo (fen_curr, fen_prev, elo, time_control) VALUES (%s, %s, %s, %s);"
        cursor.execute(query, (fen_curr, fen_prev, elo, time_control))
    except psycopg2.Error as e:
        print(f"Error inserting data into the database: {e}")

# Main function to process the PGN file and insert data into the database
def process_pgn_file(file_path):
    try:
        with open(file_path) as file:
            pgn_text = file.read()
    except IOError as e:
        print(f"Error reading file {file_path}: {e}")
        return

    pgn_io = io.StringIO(pgn_text)
    game = chess.pgn.read_game(pgn_io)

    while game:
        try:
            board = game.board()
            fen_prev = None
            time_control = game.headers.get("TimeControl", "unknown")

            for move in game.mainline_moves():
                board.push(move)

                fen_curr = board.fen()
                elo_key = 'WhiteElo' if board.turn == chess.BLACK else 'BlackElo'
                if elo_key not in game.headers or not game.headers[elo_key].isdigit():
                    fen_prev = fen_curr
                    continue
                elo = int(game.headers[elo_key])

                conn = connect_to_db()
                if conn:
                    try:
                        cursor = conn.cursor()
                        insert_data(cursor, fen_curr, fen_prev, elo, time_control)
                        conn.commit()
                    except Exception as e:
                        print(f"Error during database operation: {e}")
                    finally:
                        cursor.close()
                        conn.close()

                fen_prev = fen_curr

        except Exception as e:
            print(f"Error processing game data: {e}")

        game = chess.pgn.read_game(pgn_io)

process_pgn_file('./data/lichess_db_standard_rated_2014-09.pgn')
