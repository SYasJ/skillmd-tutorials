# dupcols.py - the pattern from NVIDIA/auto-ontology issue #408, in plain Python.
# Our own code (stdlib only), NOT Auto Ontology's. MIT, skill.md ep014.
# 15 lines of code: two tables, one join, two columns named id, two named name.
import sqlite3; db = sqlite3.connect(":memory:")
db.executescript("CREATE TABLE customers (id INT, name TEXT); CREATE TABLE orders (id INT, customer_id INT, name TEXT);"
                 "INSERT INTO customers VALUES (1, 'Ada'); INSERT INTO orders VALUES (100, 1, 'first order');")

# run(): print the column names, the raw row tuple,
# and the same row turned into a dict keyed by column name
# (the way many database connectors build result rows).


def run(sql):
    cur = db.execute(sql)
    cols = [d[0] for d in cur.description]
    row = cur.fetchone()
    print("columns :", cols)
    print("raw row :", row)
    print("as dict :", dict(zip(cols, row)))  # one dict per row, keyed by column name
    print()

print("1) same column names, no error:")
run("SELECT c.id, o.id, c.name, o.name FROM customers c JOIN orders o ON o.customer_id = c.id")
print("2) fix: give every column its own name:")
run("SELECT c.id AS customer_id, o.id AS order_id, c.name AS customer, o.name AS order_name FROM customers c JOIN orders o ON o.customer_id = c.id")
