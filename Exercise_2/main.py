import sqlite3
import os

# Function to create the database and table if they don't exist in the Exercise_2 folder
def create_database_and_table():
    db_path = os.path.join("Exercise_2", "stephen_king_adaptations.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS stephen_king_adaptations_table (
                    movieID INTEGER PRIMARY KEY,
                    movieName TEXT,
                    movieYear INTEGER,
                    imdbRating REAL)''')

    conn.commit()
    conn.close()

# Function to read the file and copy its content to a list
def read_file_to_list():
    stephen_king_adaptations_list = []
    with open(os.path.join("Exercise_2", "stephen_king_adaptations.txt"), "r") as file:
        for line in file:
            movie_info = line.strip().split(",")
            if len(movie_info) == 4:  # Check if there are four data items (including movie ID)
                movie_name, movie_year, imdb_rating = movie_info[1], int(movie_info[2]), float(movie_info[3])
                stephen_king_adaptations_list.append((movie_name, movie_year, imdb_rating))  # Exclude movie ID

    return stephen_king_adaptations_list

# Function to populate the database with data from the list
def populate_database_from_list(data_list):
    db_path = os.path.join("Exercise_2", "stephen_king_adaptations.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for movie_data in data_list:
        movie_name, movie_year, imdb_rating = movie_data
        # Check if the movie with the same name and year already exists in the database
        cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName = ? AND movieYear = ?", (movie_name, movie_year))
        existing_movie = cursor.fetchone()
        if existing_movie is None:
            cursor.execute("INSERT INTO stephen_king_adaptations_table (movieName, movieYear, imdbRating) VALUES (?, ?, ?)", (movie_name, movie_year, imdb_rating))

    conn.commit()
    conn.close()

# Function to print movie details in a formatted manner
def print_movie_details(movie):
    print("\n\tMovie ID:", movie[0])
    print("\tMovie Name:", movie[1])
    print("\tMovie Year:", movie[2])
    print("\tIMDB Rating:", movie[3])

# Function to search for movies in the database
def search_movies():
    db_path = os.path.join("Exercise_2", "stephen_king_adaptations.db")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    while True:
        print("\nOptions:")
        print("1. Search by movie name")
        print("2. Search by movie year")
        print("3. Search by movie rating")
        print("4. STOP")

        choice = input("Enter your choice: ")

        if choice == "1":
            movie_name = input("Enter the movie name: ")
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieName = ?", (movie_name,))
            movies = cursor.fetchall()
            if movies:
                for movie in movies:
                    print_movie_details(movie)
            else:
                print("\nNo such movie exists in our database")

        elif choice == "2":
            movie_year = input("Enter the movie year: ")
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE movieYear = ?", (movie_year,))
            movies = cursor.fetchall()
            if movies:
                for movie in movies:
                    print_movie_details(movie)
            else:
                print("\nNo movies were found for that year in our database")

        elif choice == "3":
            rating = input("Enter the minimum IMDB rating: ")
            cursor.execute("SELECT * FROM stephen_king_adaptations_table WHERE imdbRating >= ?", (rating,))
            movies = cursor.fetchall()
            if movies:
                for movie in movies:
                    print_movie_details(movie)
            else:
                print("\nNo movies at or above that rating were found in the database")

        elif choice == "4":
            break

    conn.close()

if __name__ == "__main__":
    create_database_and_table()
    stephen_king_adaptations_list = read_file_to_list()
    populate_database_from_list(stephen_king_adaptations_list)
    search_movies()
