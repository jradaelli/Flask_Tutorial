from flask import Flask, request, render_template, redirect
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app_lulu = Flask(__name__)

app_lulu.vars = {}
app_lulu.questions = {}

app_lulu.questions['How many eyes do you have?'] = ('1', '2', '3')
app_lulu.questions['Which fruit do you like best?'] = (
    'banana', 'mango', 'pineapple')
app_lulu.questions['Do you like cupcakes?'] = ('yes', 'no', 'maybe')

app_lulu.nquestions = len(app_lulu.questions)
logger.info(app_lulu.questions)
logger.info('NUMERO DOMANDE DA FARE: %s' % (app_lulu.nquestions))


@app_lulu.route('/')
def main_page_lulu():
    return redirect('/index_lulu')


@app_lulu.route('/index_lulu', methods=['GET', 'POST'])
def index_lulu_function():
    num_question = app_lulu.nquestions
    if request.method == 'GET':
        return render_template('userinfo_lulu.html', num=num_question)
    else:
        # save variables
        app_lulu.vars['name'] = request.form['name_lulu']
        app_lulu.vars['age'] = request.form['age_lulu']
        # log
        logger.info('INPUT - NAME: %s AGE: %s' %
                    (app_lulu.vars['name'], app_lulu.vars['age']))

        # write
        f = open('Output//%s_%s.txt' %
                 (app_lulu.vars['name'], app_lulu.vars['age']), 'w')
        f.write('Name: %s\n' % (app_lulu.vars['name']))
        f.write('Age: %s\n' % (app_lulu.vars['age']))

        logger.info('Successfully written in output folder')
        f.close()

        return redirect('/main_lulu')


@app_lulu.route('/main_lulu')
def main_lulu_function():
    if len(app_lulu.questions) == 0:
        return render_template('endfile_lulu.html')
    return redirect('/next_lulu')


@app_lulu.route('/next_lulu', methods=['GET'])
def next_lulu():
    n = app_lulu.nquestions - len(app_lulu.questions) + 1
    q = app_lulu.questions.keys()[0]
    a1, a2, a3 = app_lulu.questions.values()[0]

    logger.info('NUMERO DOMANDA: %s' % (n))
    logger.info('DOMANDA: %s' % (q))
    logger.info('RISPOSTE: %s, %s, %s' % (a1, a2, a3))

    app_lulu.currentq = q

    return render_template('layout_lulu.html', num=n, question=q,
                           ans1=a1, ans2=a2, ans3=a3)


@app_lulu.route('/next_lulu', methods=['POST'])
def next_lulu2():
    f = open('Output//%s_%s.txt' %
             (app_lulu.vars['name'], app_lulu.vars['age']), 'a')
    f.write('%s\n' % (app_lulu.currentq))
    f.write('%s\n\n' % (request.form['answer_from_layout_lulu']))
    f.close()

    logger.info('DOMANDA DA CANCELLARE: %s' %
                (str(app_lulu.questions[app_lulu.currentq])))

    del app_lulu.questions[app_lulu.currentq]
    return redirect('/main_lulu')

if __name__ == '__main__':
    app_lulu.run(port=33507, debug=True)
