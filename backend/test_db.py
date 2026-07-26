import psycopg2

try:
    print("Trying to connect...")

    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="medical_assistant",
        user="postgres",
        password="LIKITH2233"   # Replace with your actual password
    )

    print("✅ Connected successfully!")

    conn.close()
    print("Connection closed.")

except Exception as e:
    print("❌ Error:")
    print(e)