Add alpha, gamma and epsilon columns to AI (db.Float for alpha/gamma; check the type for epsilon, since PARAMS says int). db.create_all() only creates tables that don’t exist yet. It won’t add columns to an existing table, so delete the SQLite file (or migrate) after changing the model.

In the evaluation() view (views.py:49), get the user’s most recent AI row, for example by ordering current_user.ais by id, or with AI.query.filter_by(user_id=current_user.id).order_by(AI.id.desc()).first(). Pass it to render_template("evaluation.html", ai=latest).

In evaluation.html, fill the sidebar on the server with Jinja, e.g. <h5 id="evalAlpha">{{ ai.alpha }}</h5>. Handle ai being None for a user who hasn’t trained yet.