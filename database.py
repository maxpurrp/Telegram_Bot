import pymysql.cursors
from config import host, user, password, db_name


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
                insert_collections = f"insert into collections (id, name_coll) values ('{id}', '{name_coll}');"
                insert_images = f"insert into images (id, name_coll, descr, image) values ('{id}','{name_coll}', '{descr}', '{img}');"
                cursor.execute(insert_collections)
                cursor.execute(insert_images)
                self.connector.commit()
                print('succesfully insert')
                return True
        except Exception as e:
            print(e)
            return False

    def add_image(self, id :int, name_coll : str, descr : str, img : str) -> bool:
        try:
            with self.connector.cursor() as cursor:
                insert_image = f"insert into images (id, name_coll, descr, image) values ('{id}','{name_coll}', '{descr}', '{img}');"
                cursor.execute(insert_image)
                self.connector.commit()
                print('succesfully adding')
                return True
        except Exception as e:
            print(e)    
            return False

    def show_collection(self, id : int) -> list:
            output = []
            cursor = self.connector.cursor()
            all_collection_user = f'select name_coll from collections where id = {id};'
            cursor.execute(all_collection_user)
            result = cursor.fetchall()
            for elem in result:
                 output.append(elem['name_coll'])
            return output

    def _check_collections(self, id : int, name_coll : str) -> bool:
        try:
            with self.connector.cursor() as cursor:
                    all_collection_user = f'select name_coll from collections where id = {id};'
                    cursor.execute(all_collection_user)
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
                    all_collection_user = f"select descr from images where id = '{id}' and name_coll = '{name_coll}';"
                    cursor.execute(all_collection_user)
                    result = cursor.fetchall()
                    output = []
                    for elem in result:
                        output.append(elem['descr'])
                    return output
        except Exception as e:
            print(e)

    def get_image(self,id : int, descr : str) -> str:
        try:
            with self.connector.cursor() as cursor:
                    all_collection_user = f"select image from images where id = '{id}' and descr = '{descr}';"
                    cursor.execute(all_collection_user)
                    result = cursor.fetchone()
                    result = result['image']
                    return result
        except Exception as e:
            print(e)

    def delete_all_coll(self, list_coll : list, id : int) -> bool:
        try:
            with self.connector.cursor() as cursor:
                    for elem in list_coll:
                        delete_from_images = f"delete from images where name_coll = '{elem}' and id = '{id}';"
                        cursor.execute(delete_from_images)
                    delete_from_collections = f"delete from collections where id = '{id}';"
                    cursor.execute(delete_from_collections)
                    self.connector.commit()
                    return True
        except Exception as e:
            print(e)
            return False
        
    def delete_one_coll(self, name_coll : str, id : int) -> bool:
        try:
            with self.connector.cursor() as cursor:
                    delete_from_images = f"delete from images where name_coll = '{name_coll}' and id = '{id}';"
                    cursor.execute(delete_from_images)
                    delete_from_collections = f"delete from collections where name_coll = '{name_coll}';"
                    cursor.execute(delete_from_collections)
                    self.connector.commit()
                    return True
        except Exception as e:
            print(e)
            return False