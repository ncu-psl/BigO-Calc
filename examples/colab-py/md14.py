def db_connection(db_name, uid, pw):
    return 'Provider=sqloledb;Server=.\SQLEXPRESS;User ID={};Password={};Database={};'.format(uid, pw, db_name)
def main():
    print(db_connection('yahoo', 'root', 8888))