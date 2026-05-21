import psycopg2

def insert_questions(questions):
    conn = psycopg2.connect(
        host="localhost",
        database="opo_enfermeria",
        user="postgres",
        password="admin",
        port="5432"
    )
    cursor = conn.cursor()
    
    for question in questions:
        cursor.execute("""
            INSERT INTO questions (question, options, correct_answer, region_id)
            VALUES (%s, %s, %s, %s)
        """, (
            question["question"],
            question["options"],
            question["correct"],
            question["region_id"],
        ))
    
    conn.commit()
    cursor.close()
    conn.close()