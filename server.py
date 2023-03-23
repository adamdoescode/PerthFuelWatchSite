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
    data = backend.get_fuel(1, 25)
    fuelTableDf = backend.getFuelReturnDf(data)
    fuelTableHTML = backend.fueldfToHTML(fuelTableDf)
    print(f'Here is the data: {str(data)[:50]}')
    print(f'Here is the request args: {request.args}')
    # render data into the template
    # return '''
    # <form action="/my-link/">
    #     <input type="submit", value="Click Me!">
    #     <input name="wow", value="wut!">
    # </form>
    # ''' + str(data)
    return render_template('fuel_table.html', data=fuelTableHTML)

if __name__ == '__main__':
    app.run(debug=True)
