from flask import Flask, request, render_template, redirect
# import logging

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)

app = Flask(__name__)

app.vars = {}
app.questions = {}

app.questions['How many eyes do you have?'] = ('1', '2', '3')
app.questions['Which fruit do you like best?'] = (
    'banana', 'mango', 'pineapple')
app.questions['Do you like cupcakes?'] = ('yes', 'no', 'maybe')

app.nquestions = len(app.questions)
# logger.info(app.questions)
# logger.info('NUMERO DOMANDE DA FARE: %s' % (app.nquestions))


@app.route('/')
def main_page_lulu():
    return redirect('/index_lulu')


@app.route('/index_lulu', methods=['GET', 'POST'])
def index_lulu_function():
    num_question = app.nquestions
    if request.method == 'GET':
        return render_template('userinfo_lulu.html', num=num_question)
    else:
        # save variables
        app.vars['name'] = request.form['name_lulu']
        app.vars['age'] = request.form['age_lulu']
        # log
        # logger.info('INPUT - NAME: %s AGE: %s' %
                    # (app.vars['name'], app.vars['age']))

        # write
        f = open('Output//%s_%s.txt' %
                 (app.vars['name'], app.vars['age']), 'w')
        f.write('Name: %s\n' % (app.vars['name']))
        f.write('Age: %s\n' % (app.vars['age']))

        # logger.info('Successfully written in output folder')
        f.close()

        return redirect('/main_lulu')


@app.route('/main_lulu')
def main_lulu_function():
    if len(app.questions) == 0:
        return render_template('endfile_lulu.html')
    return redirect('/next_lulu')


@app.route('/next_lulu', methods=['GET'])
def next_lulu():
    n = app.nquestions - len(app.questions) + 1
    q = app.questions.keys()[0]
    a1, a2, a3 = app.questions.values()[0]

    # logger.info('NUMERO DOMANDA: %s' % (n))
    # logger.info('DOMANDA: %s' % (q))
    # logger.info('RISPOSTE: %s, %s, %s' % (a1, a2, a3))

    app.currentq = q

    return render_template('layout_lulu.html', num=n, question=q,
                           ans1=a1, ans2=a2, ans3=a3)


@app.route('/next_lulu', methods=['POST'])
def next_lulu2():
    f = open('Output//%s_%s.txt' %
             (app.vars['name'], app.vars['age']), 'a')
    f.write('%s\n' % (app.currentq))
    f.write('%s\n\n' % (request.form['answer_from_layout_lulu']))
    f.close()

    # logger.info('DOMANDA DA CANCELLARE: %s' %
                # (str(app.questions[app.currentq])))

    del app.questions[app.currentq]
    return redirect('/main_lulu')

if __name__ == '__main__':
    app.run()
