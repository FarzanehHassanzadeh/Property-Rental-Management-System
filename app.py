from flask import Flask, request, render_template, redirect

app = Flask('__name__')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return render_template('Login-Page.html')

    return render_template('welcome.html')


if __name__ == '__main__':
    app.run(debug=True)
