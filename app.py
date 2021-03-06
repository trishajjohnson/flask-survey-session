from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES = "responses"


@app.route('/')
def home_page():
    
    """Shows homepage with start survey button"""
    
    return render_template('start_survey.html', survey=survey)


@app.route('/start-survey', methods=["POST"])
def start_survey():

    """Clears RESPONSES of previous answers, sets to an empty list.  Then redirects to first question of survey."""

    session[RESPONSES] = []
    
    return redirect('/questions/0')


@app.route('/answer', methods=["POST"])
def handle_answer():

    """Retrieves answer from form, appends answer to RESPONSES list and redirects to next question"""

    answer = request.form["answer"]
    responses = session[RESPONSES]
    responses.append(answer)
    session[RESPONSES] = responses
    
    if len(session[RESPONSES]) < len(survey.questions):
        num = len(session[RESPONSES])
        return redirect(f'/questions/{num}')

    else:
        return redirect('/survey-complete')



@app.route('/questions/<int:qnum>')
def display_question(qnum):

    """Takes you to the first question of the survey after the start button is clicked"""
    
    # breakpoint()
    if session[RESPONSES] is None:
        flash("Please click Start Survey!")
        return redirect('/')

    elif len(session[RESPONSES]) == len(survey.questions):
        flash("You have already completed the survey, thank you!")
        flash("If you'd like to take another survey, please click Return Home!")
        return redirect('/survey-complete')

    elif len(session[RESPONSES]) == 0 and qnum > 0 and qnum < len(survey.questions):
        flash("Please click Start Survey and take questions in order!")
        return redirect('/')

    elif len(session[RESPONSES]) == 0 and qnum >= len(survey.questions):
        flash(f"There is only { len(survey.questions) } questions in the survey. Question #{qnum + 1} does not exist.")
        flash("Please click Start Survey and take survey questions in order!")
        return redirect('/')

    elif len(session[RESPONSES]) > 0 and len(session[RESPONSES]) < len(survey.questions) and qnum >= len(survey.questions):
        flash(f"There is only { len(survey.questions) } questions in the survey. Question #{qnum + 1} does not exist.")
        flash("Please take survey questions in order!")
        return redirect(f'/questions/{ len(session[RESPONSES]) }')

    elif len(session[RESPONSES]) != qnum:
        flash("Please take survey questions in order!")
        return redirect(f'/questions/{ len(session[RESPONSES]) }')
    
    
    question = survey.questions[qnum]

    return render_template('question.html', num=qnum, question=question)


@app.route('/survey-complete')
def survey_complete_msg():

    """"Displays survey complete message once survey has been completed"""
   
    return render_template('survey-complete.html')