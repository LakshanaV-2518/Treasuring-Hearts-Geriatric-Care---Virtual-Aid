import mysql.connector

def execute_query(query, params=None, fetchone=False):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(query, params)

        if fetchone:
            result = cursor.fetchone()
        else:
            result = cursor.fetchall()

        connection.commit()
        return result
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
    finally:
        cursor.close()
        connection.close()