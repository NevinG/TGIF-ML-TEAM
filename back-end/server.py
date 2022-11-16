from tensorflow import keras
model = keras.models.load_model('./the_model')

#import and clean bill data
import pandas as pd
bill_data = pd.read_csv('bill_data.csv')
bill_data["house_bill"] = bill_data["house_bill"].astype(int)
bill_data["senate_bill"] = bill_data["senate_bill"].astype(int)
bill_data["passed"] = bill_data["passed"].astype(int)

def makePrediction(leg_sess, bill_type, bill_num):
    bill = bill_data.loc[(bill_data['legislative_session'] == leg_sess) & (bill_data[bill_type] == 1) & (bill_data['bill_number'] == bill_num)]
    bill.pop('bill_number')
    bill.pop('legislative_session')
    bill.pop('passed')

    prediction = model.predict(bill)
    return prediction[0][0]

print(makePrediction('84R', 'house_bill', 701))


#server code

from flask import Flask, json, request
from flask_cors import CORS

api = Flask(__name__)
CORS(api)

@api.route('/predict_bill', methods=['GET'])
def get_bill_prediction():
    try:
        args = request.args
        args.to_dict()

        leg_sess = args.get("leg_sess")
        bill_type = args.get("bill_type")
        bill_num = int(args.get("bill_num"))
    
        prediction = makePrediction(leg_sess, bill_type, bill_num)
        return {"prediction": str(prediction)}
    except Exception as error:
        print(error)
        return "incorrect bill information", 400

if __name__ == '__main__':
    api.run() 