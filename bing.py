from flask import Flask, send_file, request,jsonify
from flask_cors import CORS 
from bing_background.bing import Bing as b
import requests
import datetime
import os

app = Flask(__name__)
CORS(app) 

@app.route('/bing')
@app.route('/bing/<int:day>')
def show_bing_url(day=0):

    #url of current day
    if day == 0: 
        result = b().get_image_url(0)
    #list: urls of previous days
    else: 
        result = b().get_list_of_urls(start=1, end=day)

    content_type = request.headers.get('Content-Type')  #request.mimetype
    if content_type == 'application/json':

        if day>0:
            res_dict = {}
            for i in range(day):
                res_dict[i] = result[i]
            result = res_dict
            
        json_response = jsonify(result)
        # response.headers.add('Access-Control-Allow-Origin', '*')
        return json_response
    else:
        return str(result)


@app.route('/bing/load')
@app.route('/bing/load/<int:day>')
def show_image(day=0):
    
    image_name = ''
    today = datetime.date.today()
    if day == 0:
        image_name = str(today) + ".jpg"
    else:
        pre_date_str = today - datetime.timedelta(days=day)
        image_name = str(datetime.datetime.strftime(pre_date_str, "%Y-%m-%d")) + ".jpg"
    file_path = os.path.expanduser("~") + "/Pictures/.bing-images/"+image_name
    if not os.path.isfile(file_path):
        msg=b(day).get_image_url(1)
        print(msg)
    return send_file(file_path)

if __name__ == "__main__":
    app.run(debug = True)
