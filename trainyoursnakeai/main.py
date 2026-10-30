from website import create_app, socketio

app = create_app()

socketio.run(app,
             port=5002,                     # avoid using default port 5000 since that's busy on Mac sometimes
             debug=True,
             allow_unsafe_werkzeug=True,    # this is not a production-level app
             )
