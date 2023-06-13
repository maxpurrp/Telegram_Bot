import pymysql.cursors
import time
from config import host, user, password, db_name

def get_time() -> str:
    seconds = time.time()
    cur_time = time.localtime(seconds)
    datetime = f'{cur_time.tm_year}-{cur_time.tm_mon}-{cur_time.tm_mday} {cur_time.tm_hour}:{cur_time.tm_min}:{cur_time.tm_sec}'
    return datetime

class Database():
    def __init__(self) -> None:
        connection = pymysql.Connect(
            host = host,
            port = 3306,
            user = user,
            password = password,
            database= db_name,
            cursorclass = pymysql.cursors.DictCursor)
        self.connector = connection

    def _start(self):
        try:
            cursor = self.connector.cursor()
            create_table_collections = 'create table if not exists collections (id int not null , name_coll varchar(32) not null , primary key (id, name_coll));'
            create_table_images = 'create table if not exists images (id int not null,name_coll varchar(32) not null, descr varchar(32) not null, image longtext not null, foreign key (id, name_coll) references collections (id, name_coll)) ;'
            cursor.execute(create_table_collections)
            cursor.execute(create_table_images)
            self.connector.commit()
            print('DB succefully connected')
        except Exception as e:
            print(e)

    def create_collection(self, id : int, name_coll : str, descr : str, img : str) -> bool:
        try:
            with self.connector.cursor() as cursor:
                cursor.execute("insert into collections values (%s, %s);", (id, name_coll))
                cursor.execute("insert into images values (%s, %s, %s, %s, %s)", (id, name_coll, descr, img, get_time()))
                self.connector.commit()
                print('succesfully insert')
                return True
        except Exception as e:
            print(e)
            return False

    def add_image(self, id :int, name_coll : str, descr : str, img : str) -> bool:
        try:
            with self.connector.cursor() as cursor:
                cursor.execute("insert into images values (%s, %s, %s, %s, %s)", (id, name_coll, descr, img, get_time()))
                self.connector.commit()
                print('succesfully adding')
                return True
        except Exception as e:
            print(e)    
            return False

    def show_collection(self, id : int) -> list:
            output = []
            cursor = self.connector.cursor()
            cursor.execute('select name_coll from collections where id = %s;', (id))
            result = cursor.fetchall()
            for elem in result:
                 output.append(elem['name_coll'])
            return output

    def _check_collections(self, id : int, name_coll : str) -> bool:
        try:
            with self.connector.cursor() as cursor:
                    cursor.execute('select name_coll from collections where id = %s;', (id,))
                    result = cursor.fetchall()
                    for elem in result:
                        if name_coll == elem['name_coll'] :
                            return False
                    return True
        except Exception as e:
            print(e)

    def _get_descriptions(self,id : int, name_coll : str) -> list:
        try:
            with self.connector.cursor() as cursor:
                    cursor.execute("select descr from images where id = %s and name_coll = %s;", (id, name_coll))
                    result = cursor.fetchall()
                    output = []
                    for elem in result:
                        output.append(elem['descr'])
                    return output
        except Exception as e:
            print(e)

    def get_image(self,id : int, descr : str) -> dict:
        try:
            with self.connector.cursor() as cursor:
                    cursor.execute("select image, time from images where id = %s and descr = %s;", (id, descr))
                    result = cursor.fetchone()
                    return result
        except Exception as e:
            print(e)

    def delete_all_coll(self, list_coll : list, id : int) -> bool:
        try:
            with self.connector.cursor() as cursor:
                    for elem in list_coll:
                        cursor.execute("delete from images where name_coll = %s and id = %s;", (elem, id))
                    cursor.execute("delete from collections where id = %s;", (id,))
                    self.connector.commit()
                    return True
        except Exception as e:
            print(e)
            return False
        
    def delete_one_coll(self, name_coll : str, id : int) -> bool:
        try:
            with self.connector.cursor() as cursor:
                    cursor.execute("delete from images where name_coll = %s and id = %s;", (name_coll, id))
                    cursor.execute("delete from collections where name_coll = %s;", (name_coll,))
                    self.connector.commit()
                    return True
        except Exception as e:
            print(e)
            return False