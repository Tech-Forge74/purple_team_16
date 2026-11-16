"""
ProofLife - local standalone version.

A tiny Flask server backed by a SQLite file (prooflife.db) that lives
right next to this script. Run it, open the printed URL, and every
"Add a record" / "Check history" action reads and writes that file.

No internet connection needed after you have Python + Flask installed.
Two people on the same Wi-Fi can both use it: whoever runs this script
can share their machine's local IP (printed on startup) so a second
phone/laptop on the same network can open it too -- all talking to the
same database file on the host machine.

Run:
    python3 app.py

Then open the URL it prints (usually http://127.0.0.1:5000).
"""

import sqlite3
import time
import re
from pathlib import Path

from flask import Flask, g, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "prooflife.db"
STATIC_DIR = BASE_DIR / "static"

app = Flask(__name__, static_folder=None)

ID_RE = re.compile(r"^[A-Z0-9][A-Z0-9\-]{1,31}$")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS products (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            created_at INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id TEXT NOT NULL,
            type TEXT NOT NULL,
            by_name TEXT NOT NULL,
            note TEXT,
            created_at INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );

        CREATE INDEX IF NOT EXISTS idx_events_product
            ON events(product_id, created_at DESC);
        """
    )
    db.commit()
    db.close()


def normalize_id(raw):
    return re.sub(r"\s+", "", (raw or "").strip().upper())


VALID_EVENT_TYPES = {"registered", "sold", "repaired", "damaged", "lost"}


@app.route("/")
def index():
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/api/products/<product_id>", methods=["GET"])
def get_product(product_id):
    pid = normalize_id(product_id)
    db = get_db()
    row = db.execute("SELECT * FROM products WHERE id = ?", (pid,)).fetchone()
    if row is None:
        return jsonify({"exists": False}), 404

    events = db.execute(
        "SELECT type, by_name AS by, note, created_at AS createdAt "
        "FROM events WHERE product_id = ? ORDER BY created_at DESC",
        (pid,),
    ).fetchall()

    return jsonify(
        {
            "exists": True,
            "id": pid,
            "name": row["name"],
            "createdAt": row["created_at"],
            "events": [dict(e) for e in events],
        }
    )


@app.route("/api/products/<product_id>/events", methods=["POST"])
def add_event(product_id):
    pid = normalize_id(product_id)
    if not ID_RE.match(pid):
        return jsonify({"error": "Invalid product ID."}), 400

    body = request.get_json(silent=True) or {}
    event_type = body.get("type", "")
    by_name = (body.get("by") or "").strip()
    note = (body.get("note") or "").strip()
    name = (body.get("name") or "").strip()

    if event_type not in VALID_EVENT_TYPES:
        return jsonify({"error": "Invalid event type."}), 400
    if not by_name:
        return jsonify({"error": "Your name / shop is required."}), 400

    now = int(time.time() * 1000)
    db = get_db()

    existing = db.execute("SELECT id FROM products WHERE id = ?", (pid,)).fetchone()
    if existing is None:
        db.execute(
            "INSERT INTO products (id, name, created_at) VALUES (?, ?, ?)",
            (pid, name or "(unnamed item)", now),
        )
    elif name:
        db.execute(
            "UPDATE products SET name = ? WHERE id = ? AND name = '(unnamed item)'",
            (name, pid),
        )

    db.execute(
        "INSERT INTO events (product_id, type, by_name, note, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (pid, event_type, by_name, note, now),
    )
    db.commit()
    return jsonify({"ok": True}), 201


if __name__ == "__main__":
    init_db()
    import socket

    hostname = socket.gethostname()
    try:
        lan_ip = socket.gethostbyname(hostname)
    except Exception:
        lan_ip = None

    print("ProofLife (local) is running.")
    print("  On this computer:  http://127.0.0.1:5000")
    if lan_ip and not lan_ip.startswith("127."):
        print(f"  On your Wi-Fi:     http://{lan_ip}:5000")
    print(f"  Database file:     {DB_PATH}")

    app.run(host="0.0.0.0", port=5000, debug=False)
