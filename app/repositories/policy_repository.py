from database.connection import connection


def get_policy(topic: str):
    result = connection.execute(
        """
        SELECT content
        FROM policies
        WHERE topic = %s
        """,
        (topic,)
    )

    row = result.fetchone()
    if row:
        return row[0]

    return None
if __name__ == "__main__":
    result = get_policy("annual_leave")
    print(result)