from postgres.postgres import create_worker_db, update_worker_db
from utils.GlobalVariables import workers
from utils.constants import WEEKS_NAME
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
from calculation.calculation import get_workers_analytics, get_workers_is_come


def validate_and_create_worker(request):
    weeks_number = set()
    keys = list(request.keys())
    for key in keys:
        try:
            index = WEEKS_NAME.index(key)
            weeks_number.add(index)
            request.pop(key, None)
        except ValueError:
            pass
    if '' in [request['name'], request['f_name'], request['salary'], request['come_time'], request['leave_time'], request['face_encodings']] and len(weeks_number) != 0:
        return {**request, "alert_message": "MA`LUMOTLARNI TO`LIQ KIRITING"}
    request['come_weeks'] = weeks_number
    request['face_encodings'] = list(
        map(float, request['face_encodings'].split(',')))
    request['come_time'] = datetime.time(
        int(request['come_time'][:2]), int(request['come_time'][3:5]))
    request['leave_time'] = datetime.time(
        int(request['leave_time'][:2]), int(request['leave_time'][3:5]))
    e, request['id'] = create_worker_db(request)
    if e is not None:
        return {**request, "alert_message": str(e)}
    workers.loc[request['id']] = pd.Series(request)


def validate_and_update_worker(request):
    weeks_number = set()
    keys = list(request.keys())
    for key in keys:
        try:
            index = WEEKS_NAME.index(key)
            weeks_number.add(index)
            request.pop(key, None)
        except ValueError:
            pass
    request['come_weeks'] = weeks_number
    # request['salary'] = int(request['salary'])
    if '' in [request['name'], request['f_name'], request['salary'], request['come_time'], request['leave_time'], request['face_encodings']] and len(weeks_number) != 0:
        return {**request, "alert_message": "MA`LUMOTLARNI TO`LIQ KIRITING"}
    request['face_encodings'] = list(
        map(float, request['face_encodings'].split(',')))
    request['come_time'] = datetime.time(
        int(request['come_time'][:2]), int(request['come_time'][3:5]))
    request['leave_time'] = datetime.time(
        int(request['leave_time'][:2]), int(request['leave_time'][3:5]))
    e = update_worker_db(request)
    if e is not None:
        return {**request, "alert_message": str(e)}
    workers.loc[int(request['id'])] = pd.Series(request)


def validate_and_get_analytics(request):
    print(request)
    from_date = request.get('from_date')
    to_date = request.get('to_date')

    if not isinstance(from_date, str) or from_date == '':
        request['from_date'] = (datetime.datetime.now()-relativedelta(months=1)
                                ).strftime("%Y-%m-%d")
    if not isinstance(to_date, str) or to_date == '':
        request['to_date'] = datetime.datetime.now().strftime("%Y-%m-%d")

    try:
        request['first_penalty'] = int(request['first_penalty'])
    except:
        request['first_penalty'] = 40000
    try:
        request['remaining_penalty'] = int(request['remaining_penalty'])
    except:
        request['remaining_penalty'] = 10000

    analytics = get_workers_analytics(**request)
    print(request)
    return {**analytics, **request}


def validate_and_get_workers_is_come(request):
    from_date = request.get('from_date')
    to_date = request.get('to_date')
    if not isinstance(from_date, str) or from_date == '':
        request['from_date'] = (datetime.datetime.now()-relativedelta(months=1)
                                ).strftime("%Y-%m-%d")
    if not isinstance(to_date, str) or to_date == '':
        request['to_date'] = datetime.datetime.now().strftime("%Y-%m-%d")

    data = get_workers_is_come(**request)
    return {"data": data, **request}
