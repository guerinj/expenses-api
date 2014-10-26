from flask import Flask
from flask import jsonify, request
from flask.ext import restful
from flask.ext.pymongo import PyMongo, ObjectId

import ipdb;




app = Flask(__name__)
app.config['MONGO_DBNAME'] = "expenses"

mongo = PyMongo(app)
api = restful.Api(app)

      
class Expense(restful.Resource):

    def get(self, expense_id=None):
        if expense_id is None:
             expenses = mongo.db.expenses.find()
            exp_list = list()
            for exp in expenses :
                exp_list.append({ "value" : exp["value"], "date" : exp["_id"].generation_time, "_id" : str(exp["_id"])})
            return jsonify(expenses = exp_list)

        else :
            if not ObjectId.is_valid(expense_id):
                return ("Bad Request", 400)

            expenses = mongo.db.expenses.find({"_id" : ObjectId(expense_id)})
            if expenses.count() != 1:
                return ("Not Found", 404)
            else: 
                exp = expenses[0]

            return jsonify(value = exp["value"], _id=str(exp["_id"]), date=exp["_id"].generation_time)
    
    def post(self):
        ipdb.set_trace()
        if not 'value' in request.json or  type(request.json["value"]) not in [float, int, long]:
            return "Bad Request", 400
        expense_id = mongo.db.expenses.insert({"value": request.json["value"]})
        
        return "OK", 200

    def delete(self, expense_id = None):
        if expense_id is None:
            return "Bad Request", 400

        mongo.db.expenses.remove({"_id": ObjectId(expense_id)})
        
        return "OK", 200


api.add_resource(Expense, '/expenses/<string:expense_id>', '/expenses')


if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0')
