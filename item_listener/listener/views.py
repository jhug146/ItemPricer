from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json
import csv
import traceback
import requests
from latest_user_agents import get_latest_user_agents


DATA_LOCATION = "C:/James/ItemPricer/item_listener/data"
CSV_LOCATION = f"{DATA_LOCATION}/items.csv"
USER_AGENT = get_latest_user_agents()[0]

@csrf_exempt
def new_item(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body.decode("utf-8"))
            print(body)
            vinted_id = body["vinted_id"]
            url = body["url"]
            is_bought = body["is_bought"]
        
            save_page(url, vinted_id)
            save_to_spreadsheet(url, vinted_id, is_bought)
        except Exception as error:
            return JsonResponse({
                "status": "failure",
                "error_message": "".join(traceback.format_exception_only(error)).strip()
            })

        return JsonResponse({
            "status": "success"
        })
    
    return JsonResponse({
        "status": "failure",
        "error_message": "POST type request required"
    })


def save_page(url, vinted_id):
    response = requests.get(
        url,
        headers = {
            "User-Agent": USER_AGENT
        }
    )
    with open(local_html(vinted_id), "w", encoding="utf-8") as item_page:
        item_page.write(response.text)

def save_to_spreadsheet(url, vinted_id, is_bought):
    write_csv(
        CSV_LOCATION,
        [
            vinted_id,
            local_html(vinted_id),
            url,
            is_bought
        ]
    )

def write_csv(file, data):
    with open(file, "a", newline="") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=",")
        csvwriter.writerow(data)

def local_html(vinted_id):
    return f"{DATA_LOCATION}/webpages/item-{vinted_id}.html"
