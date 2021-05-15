import requests
from datetime import date
import json
state_districts= ["151","152"]

usefull_centers_18 = []
usefull_centers_45 = []




def get_district_centers(district_id):
    today = date.today()
    today_date_str = today.strftime("%d-%m-%Y")
    
    district_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id="+district_id+"&date="+ today_date_str
    user_agent= "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
    
    http_resp = requests.get(district_url, headers={"user-agent":user_agent})
    
    return process_api_response(http_resp)

def process_api_response(http_resp):
    resp_json = json.loads(http_resp.text)
    return resp_json["centers"]

def filter_useful_centers(centers):

    for center in centers:
        found_18 = False
        found_45 = False
        for session in center["sessions"]:
            if session["available_capacity"] >0:
                if session["min_age_limit"] == 18:
                    found_18 = True
                else:
                    found_45 = True
        if found_18:
            usefull_centers_18.append(center)
        if found_45:
            usefull_centers_45.append(center)

for d_id in state_districts:
    centers = get_district_centers(d_id)
    filter_useful_centers(centers)

print(json.dumps({"18": usefull_centers_18, "45":usefull_centers_45}))
