import numpy as np
from flask import Flask, request, jsonify, render_template
import health_insurance

app = Flask(__name__)
model = pickle.load(open('heainsu.h5', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    age = request.form.values('age')
    bmi = request.form.values('bmi')
    ob_co = request.form.values('obese_coeff')
    smoker = request.form.values('smoker')
    children = request.form.values('children')
    region = request.form.values('region')
    
    prediction = health_insurance.calculate_insurance(age, ob_co, smoker)
    print(prediction)
    
    return render_template('index.html', 
  prediction_text=
  'Health Insurance Charges: {}'.format(prediction))
if __name__ == "__main__":
    app.run(debug=True)
