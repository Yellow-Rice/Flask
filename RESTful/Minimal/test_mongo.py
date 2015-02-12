import urllib.parse
from pymongo import MongoClient
from flask import Flask, jsonify, make_response
from flask.ext.restful import reqparse, abort, Api, Resource
from bson import json_util, ObjectId
import json

app = Flask(__name__)
api = Api(app)

username = 'liuyuxiao'
password = '900315lyX'
username = urllib.parse.quote_plus(username)
password = urllib.parse.quote_plus(password)

client = MongoClient('mongodb://' + username + ':' + password + '@123.56.116.122:27017/')
db = client.schooldata
collection = db.highschool

def abort_if_school_doesnt_exist(school_name):
    if school_name == None or collection.find({'school_name' : school_name}).count() == 0:
        abort(404, message = 'School {} doesn\'t exist!'.format(school_name))

def abort_if_school_exist(school_name):
    if collection.find({'school_name' : school_name}).count() > 0:
        abort(422, message = 'School {} already exists!'.format(school_name))

school_attributes = ['Merit Scholarships Offered', 'Acceptance Rate', 'grade_text', 'Classroom Dress Code', 'Endowment Size', 'Director of Admissions', 'school_name', 'Definition of Terms\xa02014 School Data', 'SSAT Required', 'ESL Courses Offered', 'SAT range (25th-75th percentile)', 'Grades Offered', 'Offers Post-Grad Year', 'of AP/Advanced Courses Offered', 'Summer Program Offered', 'Total Extracurricular Organizations', 'Average SAT Score', 'Accepts Standardized Application', 'tel', 'Saturday Classes', 'Enrollment', 'Religious Affiliation', 'address', 'Yearly Tuition (Boarding Students)', 'School Focus', 'website', 'Average Percentile SSAT', 'enrolled', 'ADD/ADHD Support', 'Interscholastic Sports Offered', 'Students on Financial Aid', 'Year Founded', 'Teacher : Student Ratio', 'School Type', 'sports', 'Associate Director of Admissions', 'Students Boarding', 'Yearly Tuition (Day Students)', 'Application Deadline', 'Average Class Size', 'Students of Color', 'International Students', 'Faculty with Advanced Degree', 'Campus Size']#, 'Avg. Financial Aid Grant']#, '_id']

parser = reqparse.RequestParser()
for each_attribute in school_attributes:
    parser.add_argument(each_attribute, type = str)

class School(Resource):
    def get(self, school_name):
        abort_if_school_doesnt_exist(school_name)
        return jsonify(json.loads(json_util.dumps(collection.find_one({'school_name' : school_name}))))
    
    def delete(self, school_name):
        abort_if_school_doesnt_exist(school_name)
        collection.remove({'school_name' : school_name})
        return '', 204
    
    def put(self, school_name):
        abort_if_school_doesnt_exist(school_name)
        args = parser.parse_args()
        school = {}
        for each_attribute in school_attributes:
            if each_attribute in args and args[each_attribute] != None:
                school[each_attribute] = args[each_attribute]
        collection.update({'school_name' : school_name}, {'$set' : school})
        return school, 201

class SchoolList(Resource):
    def get(self):
        school_list = list(collection.find())
        response = make_response(json_util.dumps(school_list), 200)
        response.headers['Content-Type'] = 'application/json'
        response.headers['mimetype'] = 'application/json'
        return response

    def post(self):
        args = parser.parse_args()
        abort_if_school_exist(args['school_name'])
        school = {}
        for each_attribute in school_attributes:
            if each_attribute in args and args[each_attribute] != None:
                school[each_attribute] = args[each_attribute]
        collection.insert(school)
        return jsonify(json.loads(json_util.dumps(school)))

api.add_resource(SchoolList, '/schools')
api.add_resource(School, '/schools/<school_name>')

if __name__ == '__main__':
    app.run(debug = True)