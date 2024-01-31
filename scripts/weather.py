import requests
import json
import mysql.connector
from mysql.connector import errorcode


def write_data_to_db(username, password, host, file_name, db):
    try:
        mydb = mysql.connector.connect(
            user=username,
            password=password,
            host=host
        )
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE {}".format(db))
        mycursor.execute("USE {}".format(db))
        mycursor.execute(
            "CREATE TABLE locations (name VARCHAR(255), temp VARCHAR(255), country VARCHAR(255), weather_desc VARCHAR(255))")

        with open(file_name, 'r') as file:
            data = json.load(file)

        for info in data:
            kelvin_temp = float(info['main']['temp'])
            celsius_temp = kelvin_temp - 273.15

            insert = "INSERT INTO locations (name, temp, country, weather_desc) VALUES (%s, %s, %s, %s)"
            val = (info['name'], celsius_temp, info['sys']['country'], info['weather'][0]['description'])
            mycursor.execute(insert, val)

        mydb.commit()
        print("Successfully saved all data to the {} database \n".format(db))
    except mysql.connector.Error as err:
        print("Failed creating database: The name {} is invalid".format(db))
        database = input("Re-enter a Database: ")
        write_data_to_db(username, password, host, file_name, database)
    except KeyError:
        print("Failed getting data from api")
        exit(1)


def show_all_databases(username, password, host):
    try:
        mydb = mysql.connector.connect(
            user=username,
            password=password,
            host=host
        )
        mycursor = mydb.cursor()
        mycursor.execute("SHOW DATABASES")
        databases = [db[0] for db in mycursor.fetchall()]

        if not databases:
            print("No databases available.")
            return None

        print("Available databases:")
        for db in databases:
            print(db)

        selected_db = input("Enter the database you want to read from: ")
        return selected_db

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your username and password.")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: The specified database does not exist.")
        elif err.errno == 2003:
            print("Error: Can't connect to MySQL server. Make sure the server is running.")
        else:
            print("Error: {}".format(err))

        return None
    

def show_data_from_db(username, password, host_ip, selected_db):
    try:
        mydb = mysql.connector.connect(
            user=username,
            password=password,
            host=host_ip,
            database=selected_db
        )
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * from locations")
        myresult = mycursor.fetchall()
        
        print("\nData from {} database:".format(selected_db))
        for x in myresult:
            print(x)
            
    except mysql.connector.ProgrammingError as err:
        if err.errno == errorcode.ER_SYNTAX_ERROR:
            print("Check your syntax!")
        else:
            print("Error: {}".format(err))


def fetch_weather_report(file_name):
    def validate_location(location, pos):
        complete_url = base_url + "appid=" + api_key + "&q=" + location
        response = requests.get(complete_url)
        data = response.json()
        if (data['cod'] != '404'):
            locations.append(data)
        else:
            print(data['message'])
            city_name = input("Re-enter {} location: ".format(pos))
            validate_location(city_name, pos)

    api_key = "3cb067f899a8c989f711fbb5e9444c3c"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    locations = []

    with open(file_name, "w") as file:
        while True:
            option = input("Enter option (1 for single location / 2 for multiple locations): ")
            
            if option == '1':
                city_name = input("Enter the name of the location: ")
                print(f"Saving location, {city_name}")
                validate_location(city_name, "single")
                break
            elif option == '2':
                positions = ['first', 'second', 'third']
                for position in positions:
                    city_name = input(
                        "Enter the name of the {} location: ".format(position))
                    print("Saving {} place...".format(position))
                    validate_location(city_name, position)
                break
            else:
                print(f"Invalid input: {option}")
                print()
                print()

        file.write(json.dumps(locations))
        file.write('\n')
    print()


def main():
    file_path = 'configuration.json'
    user = 'root'
    password = '123a'
    host = '127.0.0.1'
    
    while True:
        print("Options:")
        print("1. Check weather of a location")
        print("2. Check weather and store result in database")
        print("3. Quit")
        print()

        option = input("Enter option (1/2/3): ")

        if option == '1':
            fetch_weather_report(file_path)
            with open(file_path, 'r') as file:
                print("Pulling current weather information from backend...\n")
                data = json.load(file)
            for info in data:
                print("name:", info['name'], end="\t")
                kelvin_temp = float(info['main']['temp'])
                celsius_temp = kelvin_temp - 273.15
                print('temp (Celsius): {:.2f}'.format(celsius_temp), end="\t")
                print('country:', info['sys']['country'], end="\t")
                print('weather_desc:', info['weather'][0]['description'])
                print()
        elif option == '2':
            fetch_weather_report(file_path)
            database = input("Enter a Database you want data written to: ")
            write_data_to_db(user, password, host, file_path, database)
            read_db = (
                input('Do you wish to read data from a database[Y / N]: ')).lower()
            if read_db == 'yes' or read_db == 'y':
                selected_db = show_all_databases(user, password, host)
                if selected_db:
                    show_data_from_db(user, password, host, selected_db)
        elif option == '3':
            print("Exiting the program.\n")
            break
        else:
            print(f"Invalid value: {option}. Please enter 1, 2, or 3")
            continue
        
        retry = input("Do you want to try again? (Y/N): ").lower()
        if retry != 'y' and retry != 'yes':
            print("Exiting the program.")
            break

if __name__ == "__main__":
    main()