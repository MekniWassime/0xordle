from datetime import datetime
from flask_session import Session
from models.game_state import game_state
from utility.daily_hex_generator import get_hex_of_the_day
from utility.leaderboard_repository import leaderboard_repository
from flask import Flask, request, render_template , url_for, session, redirect

#__name__
def create_app(name):
    app = Flask(__name__)
    sess = Session(app)

    app.secret_key = 'BAD_cxvxcvSECRET_KEY'
    app.config['SESSION_TYPE'] = 'filesystem'
    sess.init_app(app)

    @app.route('/')
    def home():
        return render_template('home.html')

    @app.route('/dailyhex', methods=['GET'])
    def dailyhex_get():
        print(get_hex_of_the_day())
        state = init_state()
        return render_template('dailyhex.html', game_state=state)

    @app.route('/dailyhex', methods=['POST'])
    def dailyhex_post():
        state = init_state()
        if(state.did_win):
            return redirect(url_for("dailyhex_get"))
        user_input = request.form['user_input']
        try:
            state.play(user_input)
            if(state.did_win):
                leaderboard_repository.add_record(state.start_time, state.end_time, state.goal, len(state.attempts))
            state.write_state_to_session(session)
            return redirect(url_for("dailyhex_get"))
        except:
            return redirect(url_for("error"))

    @app.route('/leaderboard')
    def leaderboard():
        records = leaderboard_repository.fetch_records()
        return render_template('leaderboard.html', records = records)

    @app.route('/resetboard')
    def resetboard():
        session.pop('goal')
        return redirect(url_for("home"))

    @app.route('/error')
    def error():
        return redirect('error.html')

    def init_state():
        current_goal = get_hex_of_the_day().lower()
        if(('goal' in session) and (session['goal'] == current_goal)):
            return game_state.read_state_from_session(session)
        else:
            start_time = datetime.now().timestamp() * 1000
            new_state = game_state(current_goal, start_time=start_time)
            new_state.write_state_to_session(session)
            return new_state
    return app

if __name__ == "__main__":
    app = create_app(__name__)
    app.run(debug=True)