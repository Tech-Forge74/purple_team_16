ProofLife (local version)
==========================

A standalone version of the ProofLife app that runs entirely on your
own computer, with its own local database file (no internet, no
Claude account needed after setup).

WHAT YOU NEED
  - Python 3 installed
  - Flask (install once with:  pip install flask)

HOW TO RUN
  1. Open a terminal in this folder.
  2. Run:
         python3 app.py
  3. It prints a URL, usually:
         http://127.0.0.1:5000
     Open that in your browser.

WHERE THE DATA IS STORED
  A file called "prooflife.db" appears in this same folder the first
  time you run the app. That is a real SQLite database -- every
  "Add a record" and "Check history" action reads and writes to it.
  Delete that file to wipe all data and start fresh.

USING IT WITH TWO DEVICES (e.g. for a live demo)
  - Run app.py on one laptop. It also prints a "On your Wi-Fi" URL
    (something like http://192.168.x.x:5000).
  - Anyone else on the SAME Wi-Fi network can open that second URL on
    their own phone/laptop, and they will read and write the same
    database file on your laptop. This is how a "seller" and a "buyer"
    on two different phones see the same product history.
  - This only works on the same network; it will not work over the
    open internet without extra setup (e.g. deploying it to a real
    server/hosting provider).

FILES
  app.py           - the server: defines the two features
                      (add a record / check history) and the database
                      tables (products, events)
  static/index.html - the page people see in their browser
  prooflife.db      - created automatically; your actual data
