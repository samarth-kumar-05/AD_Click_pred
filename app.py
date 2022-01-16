from ast import In
from copyreg import pickle
from flask import Flask,request,escape
import pandas as pd
from flask.templating import render_template
import pickle
PredictorScaler = pickle.load(open('PredictorScaler.pkl','rb'))

# This Function can be called from any from any front end tool/website
def PredictClickStatus(InputData):
    import pandas as pd
    Num_Inputs=InputData.shape[0]
    
    # Making sure the input data has same columns as it was used for training the model
    # Also, if standardization/normalization was done, then same must be done for new input
    
    # Appending the new data with the Training data
    DataForML=pd.read_pickle('DataForML.pkl')
    InputData=InputData.append(DataForML)
    
    # Treating the binary nominal variables first
    # Every column which was converted to numeric has to be converted here as well
    InputData['Male'].replace({'Yes':1, 'No':0}, inplace=True)
    
    # Generating dummy variables for rest of the nominal variables
    InputData=pd.get_dummies(InputData)
            
    # Maintaining the same order of columns as it was during the model training
    Predictors=["Time_Spent", "Avg_Income", "Internet_Usage"]
    
    # Generating the input values to the model
    X=InputData[Predictors].values[0:Num_Inputs]    
    
    # Loading the Function from pickle file
    import pickle
    with open('finalSVM.pkl', 'rb') as fileReadStream:
        AdaBoost_model=pickle.load(fileReadStream)
        # Don't forget to close the filestream!
        fileReadStream.close()
            
    # Genrating Predictions
    Prediction=AdaBoost_model.predict(X)
    PredictedStatus=pd.DataFrame(Prediction, columns=['ClickPrediction'])
    return(PredictedStatus)

# Calling the function for some new Ads
NewAds=pd.DataFrame(
data=[[35.98,60813.00, 125.20],
     [70.96, 69874.18, 198.72],
     [56.91, 21773.22, 146.44]],
columns=["Time_Spent", "Avg_Income", "Internet_Usage"])

# Calling the Function for prediction and storing with the input data
NewAds['ClickPrediction']=PredictClickStatus(InputData= NewAds)
print(NewAds)

# Creating the function which can take Ad inputs and perform prediction
"Time_Spent", "Avg_Income", "Internet_Usage"
def FunctionClickPrediction(inp_Time_Spent, inp_Avg_Income, inp_Internet_Usage):
    SampleInputData=pd.DataFrame(
     data=[[inp_Time_Spent, inp_Avg_Income, inp_Internet_Usage]],
     columns=["Time_Spent", "Avg_Income", "Internet_Usage"])

    # Calling the function defined above using the input parameters
    Predictions=PredictClickStatus(InputData= SampleInputData)

    # Returning the predicted Clicked status
    return(Predictions)



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict',methods = ["GET","POST"])
def calc():
    if request.method == "POST":
        
            Time = str(request.form['time'])
            Income = str(request.form['income'])
            Internet = str(request.form['internet'])
            calculated = FunctionClickPrediction(float(Time),float(Income),float(Internet))
            predicted = calculated.to_string(index=False)
            predicted = int(predicted[16:])
            if(predicted == 0):
                predd = 'will not'
            elif(predicted == 1):
                predd = 'will'
            return render_template('final.html',preddicted=' '+predd)
    else:
        return render_template('pred.html')
@app.route('/result')
def result():
    return render_template('final.html')

@app.route('/about-us')
def about():
    return render_template('aboutus.html')

if(__name__ == '__main__'):
    app.run()