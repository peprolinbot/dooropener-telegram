import requests

from config import doordumbapi_base_url, doordumbapi_token, door_id, wait_to_close_time


class DoorException(Exception):
    pass


def _api_get(endpoint, params={}):
    r = requests.get(f"{doordumbapi_base_url}{endpoint}",
                     params=params,
                     headers={
                         "x-access-token": doordumbapi_token
                     },
                     )
    if r.status_code == 200:
        return r.json()["message"]
    else:
        raise DoorException(r.json()["error"]["id"])


def open_door():
    return _api_get(f"/door/{door_id}/open",
                    params={"wait_to_close_time": wait_to_close_time},
                    )


def toggle_door():
    return _api_get(f"/door/{door_id}/toggle")
