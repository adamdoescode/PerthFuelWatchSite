from flask import Flask, render_template, request
app = Flask(__name__)
import backend

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results/')
def getData():
    '''
    Returns the data from the fuelwatch RSS feed
    Using get_fuel function
    '''
    print(f'I got clicked!')
    data = backend.retrieveData() #defaults to greater Perth
    fuelTableHTML = backend.fueldfToHTML(data)
    print(f'Here is the request args: {request.args}')
    print(f'Here is the data: {str(data)[:50]}')
    print(f'Here is the HTML table: {str(fuelTableHTML)[:50]}')
    return render_template('index.html', fuelDataTable=fuelTableHTML)

if __name__ == '__main__':
    app.run(debug=True)
