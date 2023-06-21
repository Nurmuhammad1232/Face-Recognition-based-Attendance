from sqlalchemy import create_engine,MetaData,Table,insert,update
import pandas as pd
from utils.constants import POSTGRESQL_URL,ATTENDANCE_FREEZE_TIME,ATTENDANCE_EXPIRATION_TIME
import cv2
from datetime import datetime


def get_sqlalchemy_engine():
    return create_engine(POSTGRESQL_URL)


def get_worker_faces()->pd.DataFrame:
    engine = get_sqlalchemy_engine()
    sql_query = "SELECT * FROM worker_faces"
    return pd.read_sql(sql = sql_query, con = engine)

def get_workers()->pd.DataFrame:
    engine = get_sqlalchemy_engine()
    sql_query = "SELECT * FROM worker"
    return pd.read_sql(sql = sql_query, con = engine,index_col='id')

# def save_worker_face_images(user_id):
#     pathes = save_worker_images(user_id)
#     engine = get_sqlalchemy_engine()
#     metadata = MetaData(bind=engine)
#     worker_faces = Table('worker_faces', metadata, autoload=True)
#     stmt = insert(worker_faces).values({"worker_id":user_id,"face_path_1":pathes[0],"face_path_2":pathes[1],"face_path_3":pathes[2]})
#     try:
#         engine.execute(stmt)
#     except Exception:
#         stmt = update(worker_faces).values({"face_path_1":pathes[0],"face_path_2":pathes[1],"face_path_3":pathes[2]}).where(worker_faces.c.worker_id == user_id)
#         engine.execute(stmt)
        
def create_worker_db(user):
    try:
        engine = get_sqlalchemy_engine()
        metadata = MetaData(bind=engine)
        worker = Table('worker', metadata, autoload=True)
        worker = insert(worker).returning(worker.c.id)
        worker = worker.values(user)
        user_id = engine.execute(worker).fetchone()[0]
        # save_worker_face_images(user_id)
    except Exception as e:
        print(e)
        return "Ma`lumot noto`g`ri kiritildi!",None
    return None,user_id

def save_worker_images(id):
    image_pathes = []
    for index in range(3):
        image_path = DATABASE_Main_Path/str(id)
        image_path.mkdir(parents=True, exist_ok=True)
        image_path/=(str(index)+'.png')
        temp_image_path = Image_Main_Path/(str(index)+'.png')
        img = cv2.imread(str(temp_image_path))
        cv2.imwrite(str(image_path),img)
        image_pathes.append(str(image_path))
    return image_pathes


def get_attendance_data(from_date,to_date):
    engine = get_sqlalchemy_engine()
    sql_query = """
    select worker_id as id,id as attendance_id, come_datetime, is_come
        from attendance
        where come_datetime::date >= date '{from_date}'
        and come_datetime::date <= date '{to_date}';
    """
    sql_query = sql_query.format(from_date=from_date, to_date=to_date)
    return pd.read_sql(sql = sql_query, con = engine)

def update_worker_db(user):
    try:
        engine = get_sqlalchemy_engine()
        metadata = MetaData(bind=engine)
        worker = Table('worker', metadata, autoload=True)
        worker = update(worker).where(worker.c.id == user['id'])
        worker = worker.values(user)
        engine.execute(worker)
    except Exception as e:
        print(e)
        return "Ma`lumot noto`g`ri kiritildi!"
    
def delete_attendance_db(id):
    try:
        engine = get_sqlalchemy_engine()
        sql_query = "DELETE FROM attendance where id = {id}"
        sql_query = sql_query.format(id=id)
        engine.execute(sql_query)
    except Exception as e:
        print(e)


def add_attendance(data):
    engine = get_sqlalchemy_engine()
    metadata = MetaData(bind=engine)
    attendance = Table('attendance', metadata, autoload=True)
    stmt = insert(attendance).values({"worker_id":data['worker_id'],"come_datetime":data['date']+' '+data['time'],"is_come":bool(int(data['iscome'])),})
    try:
        engine.execute(stmt)
    except Exception as e:
        print(e)


def delete_worker_db(id):
    try:
        engine = get_sqlalchemy_engine()
        sql_query = "DELETE FROM worker where id = {id}"
        sql_query = sql_query.format(id=id)
        engine.execute(sql_query)
    except Exception as e:
        print(e)


def delete_attendance_time_by_id(id):
    engine = get_sqlalchemy_engine()
    sql_query = "DELETE FROM public.attendance WHERE id = {id}".format(id = id)
    engine.execute(sql_query)


def save_worker_come_time(worker_id):
    engine = get_sqlalchemy_engine()
    sql_query = """select EXTRACT(EPOCH FROM (now() - come_datetime)),is_come,id
                from attendance
                where worker_id = {worker_id}
                order by come_datetime desc
                limit 1
        """.format(worker_id = worker_id)
    result = engine.execute(sql_query).fetchone()
    is_come = True
    
    if result is not None:
        if result[0]<=ATTENDANCE_FREEZE_TIME:
            freeze_diff_time = ATTENDANCE_FREEZE_TIME - result[0]
            text = "YUZ MUZLATILGAN: "+datetime.utcfromtimestamp(freeze_diff_time).strftime('%H:%M:%S')
            return text
        
        is_come = not result[1]
        if result[1] and result[0]>=ATTENDANCE_EXPIRATION_TIME:
            delete_attendance_time_by_id(result[2])
            is_come = True

    
    sql_query = "INSERT INTO attendance(worker_id,is_come) values({worker_id},{is_come});"
    sql_query = sql_query.format(worker_id = worker_id, is_come = is_come)
    engine.execute(sql_query)
    if is_come:
        text="Kuningiz samarali o`tsin "
    else:
        text="Hayir"
    return text
