from lwsql.parser import SQLParser


def test_sql_parser():
    parser = SQLParser()

    sql1 = "CREATE TABLE students (id int, name str, age int)"
    sql2 = "INSERT INTO students VALUES (1, 'Alice', 30)"
    sql3 = "SELECT id, name FROM students"
    sql4 = (
        "SELECT id, name FROM students JOIN courses ON students.id = courses.student_id"
    )

    result1 = parser.parse(sql1)
    result2 = parser.parse(sql2)
    result3 = parser.parse(sql3)
    result4 = parser.parse(sql4)

    expected_result1 = [
        "CREATE TABLE",
        "students",
        ["id", "int"],
        ["name", "str"],
        ["age", "int"],
    ]
    expected_result2 = ["INSERT INTO", "students", "1", "Alice", "30"]
    expected_result3 = ["SELECT", "id", "name", "FROM", "students"]
    expected_result4 = [
        "SELECT",
        "id",
        "name",
        "FROM",
        "students",
        "JOIN",
        "courses",
        "ON",
        "students",
    ]

    assert result1 == expected_result1
    assert result2 == expected_result2
    assert result3 == expected_result3
    assert result4 == expected_result4
