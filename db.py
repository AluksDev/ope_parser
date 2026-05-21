import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        database="opo_enfermeria",
        user="postgres",
        password="admin",
        port="5432"
    )
    print("Connection successful")

    conn.close()

except Exception as e:
    print("Connection failed:")
    print(e)