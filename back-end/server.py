from tensorflow import keras
ml_model = keras.models.load_model('./ML_Model')

#import and clean bill data
import pandas as pd
import numpy as np

bill_data = pd.read_csv('bill_data.csv')
bill_data["house_bill"] = bill_data["house_bill"].astype(int)
bill_data["senate_bill"] = bill_data["senate_bill"].astype(int)
bill_data["passed"] = bill_data["passed"].astype(int)

from committee_dict import second_committee_to_number as committee_to_number

def makePrediction(leg_sess, bill_type, bill_num):
    bill = bill_data.loc[(bill_data['legislative_session'] == leg_sess) & (bill_data[bill_type] == 1) & (bill_data['bill_number'] == bill_num)]
    bill.pop('bill_number')
    bill.pop('legislative_session')
    bill.pop('passed')

    prediction = ml_model.predict(bill)
    return prediction[0][0]

def makePredictionCreate(committee, bill_type, joint_authors, co_authors, num_of_subjects):
    #get session information
    leg_sess_df = pd.read_csv('leg_sess_data.csv')
    session_data = leg_sess_df.loc[leg_sess_df['leg_sess'] == int("87R"[:2])]

    bill = {}

    bill["male_house_members"] = int(session_data.iloc[0]['male_house_members'])
    bill["male_senate_members"] = int(session_data.iloc[0]['male_senate_members'])
    bill["female_house_members"] = int(session_data.iloc[0]['female_house_members'])
    bill["female_senate_members"] = int(session_data.iloc[0]['female_senate_members'])
    bill["democrat_house_members"] = int(session_data.iloc[0]['democrat_house_members'])
    bill["democrat_senate_members"] = int(session_data.iloc[0]['democrat_senate_members'])
    bill["republican_house_members"] = int(session_data.iloc[0]['republican_house_members'])
    bill["republican_senate_members"] = int(session_data.iloc[0]['republican_senate_members'])
    bill["house_incumbents"] = int(session_data.iloc[0]['house_incumbents'])
    bill["senate_incumbents"] = int(session_data.iloc[0]['senate_incumbents'])
    bill["house_freshman"] = int(session_data.iloc[0]['house_freshman'])
    bill["senate_freshman"] = int(session_data.iloc[0]['senate_freshman'])
    bill["house_members_age_under_30"] = int(session_data.iloc[0]['house_members_age_under_30'])
    bill["senate_members_age_under_30"] = int(session_data.iloc[0]['senate_members_age_under_30'])
    bill["house_members_age_30_to_39"] = int(session_data.iloc[0]['house_members_age_30_to_39'])
    bill["senate_members_age_30_to_39"] = int(session_data.iloc[0]['senate_members_age_30_to_39'])
    bill["house_members_age_40_to_49"] = int(session_data.iloc[0]['house_members_age_40_to_49'])
    bill["senate_members_age_40_to_49"] = int(session_data.iloc[0]['senate_members_age_40_to_49'])
    bill["house_members_age_50_to_59"] = int(session_data.iloc[0]['house_members_age_50_to_59'])
    bill["senate_members_age_50_to_59"] = int(session_data.iloc[0]['senate_members_age_50_to_59'])
    bill["house_members_age_60_to_69"] = int(session_data.iloc[0]['senate_members_age_60_to_69'])
    bill["house_members_age_over_70"] = int(session_data.iloc[0]['house_members_age_over_70'])
    bill["senate_members_age_over_70"] = int(session_data.iloc[0]['senate_members_age_over_70'])

    bill["house_committee_democrats"] = int(session_data.iloc[0]['committee_{}_democrats'.format(committee_to_number.get(committee,0))]) if bill_type == 'house_bill' else 0

    bill["house_committee_republicans"] = int(session_data.iloc[0]['committee_{}_republicans'.format(committee_to_number.get(committee,0))]) if bill_type == 'house_bill' else 0
    bill["senate_committee_democrats"] = int(session_data.iloc[0]['committee_{}_democrats'.format(committee_to_number.get(committee,0))]) if bill_type == 'senate_bill' else 0
    bill["senate_committee_republicans"] = int(session_data.iloc[0]['committee_{}_republicans'.format(committee_to_number.get(committee,0))]) if bill_type == 'senate_bill' else 0


    #translate data to what were storing in the csv

    features = {
        "house_bill": bill_type == "house_bill",
        "senate_bill": bill_type == "senate_bill",
        "num_of_joint_authors": joint_authors,
        "num_of_co_authors": co_authors,
        "num_of_subjects": num_of_subjects,

        "male_house_members": bill["male_house_members"],
        "male_senate_members": bill["male_senate_members"],
        "female_house_members": bill["female_house_members"],
        "female_senate_members": bill["female_senate_members"],
        "democrat_house_members": bill["democrat_house_members"],
        "democrat_senate_members": bill["democrat_senate_members"],
        "republican_house_members": bill["republican_house_members"],
        "republican_senate_members": bill["republican_senate_members"],
        "house_incumbents": bill["house_incumbents"],
        "senate_incumbents": bill["senate_incumbents"],
        "house_freshman": bill["house_freshman"],
        "senate_freshman": bill["senate_freshman"],
        "house_members_age_under_30": bill["house_members_age_under_30"],
        "senate_members_age_under_30": bill["senate_members_age_under_30"],
        "house_members_age_30_to_39": bill["house_members_age_30_to_39"],
        "senate_members_age_30_to_39": bill["senate_members_age_30_to_39"],
        "house_members_age_40_to_49": bill["house_members_age_40_to_49"],
        "senate_members_age_40_to_49": bill["senate_members_age_40_to_49"],
        "house_members_age_50_to_59": bill["house_members_age_50_to_59"],
        "senate_members_age_50_to_59": bill["senate_members_age_50_to_59"],
        "house_members_age_60_to_69": bill["house_members_age_60_to_69"],
        "house_members_age_over_70": bill["house_members_age_over_70"],
        "senate_members_age_over_70": bill["senate_members_age_over_70"],
        "house_committee_democrats": bill["house_committee_democrats"],
        "house_committee_republicans": bill["house_committee_republicans"],
        "senate_committee_democrats": bill["senate_committee_democrats"],
        "senate_committee_republicans": bill["senate_committee_republicans"]
    }

    prediction = ml_model.predict(np.array([list(features.values())]))

    return prediction[0][0]




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


@api.route('/predict_bill_create', methods=['GET'])
def get_bill_prediction_create():
    try:
        args = request.args
        args.to_dict()

        committee = args.get("committee")
        bill_type = args.get("bill_type")
        joint_authors = int(args.get("joint_authors"))
        co_authors = int(args.get("co_authors"))
        num_of_subjects = int(args.get("num_of_subjects"))
    
        prediction = makePredictionCreate(committee, bill_type, joint_authors, co_authors, num_of_subjects)
        return {"prediction": str(prediction)}
    except Exception as error:
        print(error)
        return "incorrect bill information", 400

if __name__ == '__main__':
    api.run() 