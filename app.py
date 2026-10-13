from flask import Flask

app = Flask(_name_)

@app.route("/")
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Hotel PMS</title>
        <style>
            body {
                font-family: Arial;
                background: #f0f4f8;
                text-align: center;
                padding: 60px;
            }
            h1 { color: #17365d; }
            .card {
                background: white;
                padding: 30px;
                border-radius: 12px;
                max-width: 500px;
                margin: auto;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Hotel PMS</h1>
            <p>Property Management System</p>
            <h2>Welcome!</h2>
            <p>Room Management | Reservations | Check-in</p>
            <p>Your first PMS application is ready to build.</p>
        </div>
    </body>
    </html>
    """

if _name_ == "_main_":
    app.run(debug=True)
