from postgres.postgres import get_attendance_data
from utils.GlobalVariables import workers
import pandas as pd
import datetime
import numpy as np
# from utils.constants import FIRST_PENALTY, REMAINING_PENALTY


def add_10_minut_to_time(time):
    return (datetime.datetime.combine(datetime.date.today(), time) + datetime.timedelta(minutes=10)).time()


def calculation_salary_and_not_come(attendance, all_dates):
    attendance = attendance.sort_values('come_datetime')
    if not attendance.empty and attendance.iloc[-1]['is_come']:
        attendance = attendance[:-1]
    if attendance.empty or attendance.shape[0] <= 1:
        return
    leave_datetime = attendance[~(
        attendance['is_come'])]['come_datetime'].values
    attendance = attendance.loc[attendance['is_come']]
    attendance['worker_worked_hours'] = (
        leave_datetime - attendance['come_datetime'])/datetime.timedelta(hours=1)
    attendance['earned_salary'] = (
        attendance['worker_worked_hours']*attendance['salary'])-attendance['late_penalty_cost']
    attendance = all_dates.join(
        attendance.set_index('come_date'), on='come_date')
    attendance['come_weeks'] = [attendance[~pd.isna(
        attendance['come_weeks'])]['come_weeks'].iloc[0]] * len(attendance)
    attendance['id'] = [
        attendance[~pd.isna(attendance['id'])]['id'].iloc[0]] * len(attendance)
    attendance['name'] = [
        attendance[~pd.isna(attendance['name'])]['name'].iloc[0]] * len(attendance)
    attendance['f_name'] = [
        attendance[~pd.isna(attendance['f_name'])]['f_name'].iloc[0]] * len(attendance)
    attendance['come_weekday'] = pd.to_datetime(
        attendance['come_date']).dt.weekday
    attendance['is_need_come'] = attendance.apply(
        lambda x: x['come_weekday'] in x['come_weeks'], axis=1)
    attendance['status_not_come'] = pd.isna(attendance['status'])
    attendance['status'] = attendance['status'].fillna("Kelmadi")
    attendance['late_penalty_times'] = np.where(
        attendance['late_penalty_cost'] == 0, 0, attendance['late_penalty_times'])

    return attendance


def get_summary(attendance):
    need_sum_columns = ['late_penalty_times', 'late_penalty_cost', 'worker_worked_hours', 'earned_salary',
                        'status_not_come', 'status_come_with_late', 'status_come_without_late', 'status_come']
    d = {i: 'sum' for i in need_sum_columns}
    d['name'] = 'first'
    d['f_name'] = 'first'
    summary_workers = attendance.groupby(
        'id')[['name', 'f_name']+need_sum_columns].agg(d)
    summary_all = summary_workers.sum(numeric_only=True).to_dict()
    summary_workers = summary_workers.to_dict(orient='records')
    return {'summary': summary_all, 'workers': summary_workers}


def get_workers_analytics(from_date, to_date, first_penalty, remaining_penalty, **kwargs):
    attendance = get_attendance_data(from_date, to_date)
    if attendance.empty or workers.empty:
        return {}
    attendance = attendance.join(workers, on='id')
    attendance.drop(['phone', 'face_encodings'],
                    axis=1, inplace=True)
    all_dates = pd.date_range(start=from_date, end=to_date)
    all_dates = pd.DataFrame(all_dates, columns=['come_date'])
    all_dates['come_date'] = all_dates['come_date'].dt.date
    attendance['status'] = 'Keldi'
    attendance['come_weekday'] = attendance['come_datetime'].dt.weekday
    attendance['come_date'] = attendance['come_datetime'].dt.date
    attendance['is_need_come'] = attendance.apply(
        lambda x: x['come_weekday'] in x['come_weeks'], axis=1)
    attendance['can_come_time'] = attendance['come_time'].apply(
        add_10_minut_to_time)
    attendance['need_come_datetime'] = pd.to_datetime(attendance['come_date'].astype(
        str) + ' ' + attendance['can_come_time'].astype(str))
    attendance['late_time'] = attendance['come_datetime'] - \
        attendance['need_come_datetime']

    attendance['late_penalty_times'] = attendance['late_time'] / \
        datetime.timedelta(hours=1)

    attendance['late_penalty_times'] = np.where(
        attendance['late_penalty_times'] < 0, 0, attendance['late_penalty_times'])

    attendance['late_penalty_cost'] = np.where(attendance["is_come"] & attendance["is_need_come"] & (
        attendance['late_penalty_times'] > 0), first_penalty, 0)

    attendance['late_penalty_cost'] = np.where(attendance["is_come"] & attendance["is_need_come"] & (
        (attendance['late_penalty_times']) > 0), attendance['late_penalty_cost']+(
        attendance['late_penalty_times'])*remaining_penalty, attendance['late_penalty_cost'])

    attendance = attendance.groupby('id').apply(
        calculation_salary_and_not_come, all_dates=all_dates)
    
    if attendance.empty:
        return {}
    attendance.reset_index(drop=True, inplace=True)
    attendance['status_come_with_late'] = (attendance['late_penalty_cost'] != 0) & (
        ~pd.isna(attendance['late_penalty_cost']))
    attendance['status_come'] = attendance['status'] == 'Keldi'
    attendance['status'] = np.where(
        attendance['status_come_with_late'], 'Kech Keldi', attendance['status'])
    attendance['status_come_without_late'] = attendance['status'] == 'Keldi'
    summary = get_summary(attendance)
    attendance.drop(['id', 'attendance_id', 'is_come', 'come_weeks', 'come_weekday',
                     'can_come_time', 'need_come_datetime', 'late_time', 'status_come_with_late',
                     'status_come', 'status_come_without_late'],
                    axis=1, inplace=True)
    attendance = attendance.groupby('come_date').apply(
        lambda x: x.to_dict(orient='records'))
    attendance = attendance.to_dict()
    return {'summary': summary, 'attendance': attendance}


def calculation_not_come(attendance, all_dates):
    attendance = all_dates.join(
        attendance.set_index('come_date'), on='come_date')
    attendance['come_weeks'] = [attendance[~pd.isna(
        attendance['come_weeks'])]['come_weeks'].iloc[0]] * len(attendance)
    attendance['id'] = [
        attendance[~pd.isna(attendance['id'])]['id'].iloc[0]] * len(attendance)
    attendance['name'] = [
        attendance[~pd.isna(attendance['name'])]['name'].iloc[0]] * len(attendance)
    attendance['f_name'] = [
        attendance[~pd.isna(attendance['f_name'])]['f_name'].iloc[0]] * len(attendance)
    attendance['come_weekday'] = pd.to_datetime(
        attendance['come_date']).dt.weekday
    attendance['is_need_come'] = attendance.apply(
        lambda x: x['come_weekday'] in x['come_weeks'], axis=1)
    attendance = attendance[~(
        (~attendance['is_need_come']) & (pd.isna(attendance['status'])))]
    attendance['status_not_come'] = pd.isna(attendance['status'])
    attendance['status'] = attendance['status'].fillna("Kelmadi")
    return attendance


def get_workers_is_come(from_date, to_date, **kwargs):
    attendance = get_attendance_data(from_date, to_date)
    if attendance.empty or workers.empty:
        return {}
    attendance = attendance.join(workers, on='id')
    attendance.drop(['phone', 'salary', 'face_encodings'],
                    axis=1, inplace=True)
    all_dates = pd.date_range(start=from_date, end=to_date)
    all_dates = pd.DataFrame(all_dates, columns=['come_date'])
    all_dates['come_date'] = all_dates['come_date'].dt.date
    attendance['status'] = np.where(attendance['is_come'], 'Keldi', 'Ketdi')
    attendance['come_weekday'] = attendance['come_datetime'].dt.weekday
    attendance['come_date'] = attendance['come_datetime'].dt.date
    attendance['is_need_come'] = attendance.apply(
        lambda x: x['come_weekday'] in x['come_weeks'], axis=1)
    attendance = attendance.groupby('id').apply(
        calculation_not_come, all_dates=all_dates)
    attendance.reset_index(drop=True, inplace=True)
    attendance = attendance.sort_values('come_date')
    attendance.drop(['is_come', 'come_weeks', 'come_weekday',
                    'status_not_come'], axis=1, inplace=True)
    attendance = attendance.groupby('come_date').apply(
        lambda x: x.to_dict(orient='records'))
    attendance = attendance.to_dict()
    return attendance
