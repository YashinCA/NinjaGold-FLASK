from flask import Flask, render_template, request, redirect, session
import random
import datetime


app = Flask(__name__)
app.secret_key = 'keep it secret, keep it safe'


@app.route('/')
def index():
    return redirect("/process_money")


@app.route("/process_money")
def inicio():
    session['activities'] = ['']
    session['goldstatus'] = 0
    session['contador'] = 0
    session['estado'] = False
    print(session['estado'])
    return render_template("game.html", goldstatus=session['goldstatus'], contador=session['contador'], estado=session['estado'])


@app.route("/process_money", methods=['POST'])
def jugar():
    green = 'green'
    red = 'red'
    date = datetime.datetime.now()
    datemoment = f'{date.strftime("%Y")}/{date.strftime("%m")}/{date.strftime("%d")} {date.strftime("%I")}:{date.strftime("%M")} {date.strftime("%p")}'
    diccionario = [{'name': 'farm', 'min': 10, 'max': 20}, {'name': 'cave', 'min': 5, 'max': 10}, {
        'name': 'house', 'min': 2, 'max': 5}, {'name': 'casino', 'min': -50, 'max': 50}]

    for i in range(4):
        numero = 0
        if diccionario[i]["name"] == request.form['building']:
            numero = int(
                round(random.random()*(((diccionario[i]["max"])-(diccionario[i]["min"])))+(diccionario[i]["min"])))
            session['goldstatus'] += numero
            session['contador'] += 1

            if (request.form['building'] == 'farm') or (request.form['building'] == 'cave') or (request.form['building'] == 'house'):
                form = request.form['building']
                color = f'style = "color:{green} "'
                mensaje = f'<h5 {color}>Earned {numero} golds from the {form}! {datemoment}</h5>'
                session['activities'].append(mensaje)
            else:
                if((request.form['building'] == 'casino') and numero >= 0):
                    form = request.form['building']
                    color = f'style = "color:{green} "'
                    mensaje = f'<h5 {color}>Entered a {form} and win {numero} golds...you are lucky!😎💰 {datemoment}</h5>'
                    session['activities'].append(mensaje)
                else:
                    form = request.form['building']
                    color = f'style = "color:{red} "'
                    mensaje = f'<h5 {color}>Entered a {form} and lost {numero} golds... Ouch...😥 {datemoment}</h5>'
                    session['activities'].append(mensaje)
            if (session['goldstatus'] < 500):
                if((session['contador'] >= 0) and (session['contador'] < 15)):
                    session['estado'] = False
                else:
                    session['estado'] = True
                    color = f'style = "color:{red} "'
                    session['activities'] = f'<h1 {color} >😥YOU LOST😥</h1>'
                print(session['estado'])
            if (session['goldstatus'] >= 200):
                if(session['contador'] == 15):
                    session['estado'] = False
                else:
                    session['estado'] = True
                    color = f'style = "color:{green} "'
                    session['activities'] = f'<h1 {color} >😎💰YOU WIN😎💰</h1>'
                print(session['estado'])
            return render_template("game.html", goldstatus=session['goldstatus'], actividad=session['activities'], contador=session['contador'], estado=session['estado'])


if __name__ == "__main__":
    app.run(debug=True)
