import time
import json

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Content-Type': 'application/json',
    'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    'Cache-Control': 'no-cache, must-revalidate'
}


def get_imt_id(nm):
    response = requests.get('https://card.wb.ru/cards/detail?nm=' + str(nm), headers=headers)
    response.raise_for_status()
    data = json.loads(response.text)
    imt_id = data['data']['products'][0]['root']
    return imt_id


def get_last_feedback(nm):
    imt_id = get_imt_id(nm)
    payload = json.dumps({
        "imtId": imt_id,
        "take": 1,
        "random": str(time.time()),
        "skip": 0
    })
    url = "https://feedbacks.wildberries.ru/api/v1/summary/full"

    response = requests.post(url, data=payload, headers=headers)
    response.raise_for_status()

    data = json.loads(response.text)

    feedback = data['feedbacks'][0]['productValuation']

    return feedback


# print(get_last_feedback(119911966))
