import sqlite3

db = sqlite3.connect('data.db')
cur = db.cursor()


class DB():

    def check_user_registered(external_id):
        res = cur.execute(
            f'select*from user where external_id = "{external_id}" ')
        data = res.fetchone()
        if data is None:
            return False
        else:
            return True

    def add_new_user(external_id, username, firstname, lastname):
        if not DB.check_user_registered(external_id=external_id):
            cur.execute(
                f'insert into user(external_id, username, firstname, lastname) values ({external_id}, "{username}", "{firstname}", "{lastname}") '
            )
        db.commit()

    def create_info(external_id):
        cur.execute(
            f'insert into info(id,external_id, isFinished) values (Null,{external_id}, 0)'
        )
        db.commit()

    def get_last_index(external_id):
        res = cur.execute(
            f'select id from info where external_id = "{external_id}" order by id desc'
        )
        idx = res.fetchone()
        return idx[0]

    def add_credit(credit, external_id):
        idx = DB.get_last_index(external_id=external_id)
        cur.execute(f'update info set credit = "{credit}" where id = {idx}')
        db.commit()

    def add_expiary_payment(context, external_id):
        idx = DB.get_last_index(external_id=external_id)
        cur.execute(
            f'update info set expired_payment = "{context}" where id = {idx}')
        db.commit()

    def add_estate(context, external_id):
        idx = DB.get_last_index(external_id=external_id)
        cur.execute(
            f'update info set hasEstate = "{context}" where id = {idx}')
        db.commit()

    def add_car(context, external_id):
        idx = DB.get_last_index(external_id=external_id)
        cur.execute(f'update info set hasCar = "{context}" where id = {idx}')
        db.commit()

    def add_salary(context, external_id):
        idx = DB.get_last_index(external_id=external_id)
        cur.execute(
            f'update info set is_official_salary = "{context}" where id = {idx}'
        )
        db.commit()

    def add_marital_status(context, external_id):
        idx = DB.get_last_index(external_id=external_id)
        cur.execute(
            f'update info set marital_status = "{context}" where id = {idx}')
        db.commit()

    def has_phone(external_id):
        res = cur.execute(
            f'select phone from user where external_id = "{external_id}" ')
        data = res.fetchone()
        if data[0] is None:
            return True
        return False

    def add_phone(phone, external_id):
        cur.execute(
            f'update user set phone = {phone} where external_id = {external_id}'
        )
        db.commit()

    def finish_info(external_id):
        idx = DB.get_last_index(external_id=external_id)
        cur.execute(f'update info set isFinished = 1 where id = {idx}')
        db.commit()

    def has_heal_name(external_id):
        res = cur.execute(
            f'select real_name from user where external_id = "{external_id}" ')
        data = res.fetchone()
        if data[0] == None or data[0] == 'NULL':
            return True
        else:
            return False

    def add_real_name(external_id, real_name):
        cur.execute(
            f'update user set real_name = "{real_name}" where external_id = {external_id}'
        )
        db.commit()

    def delete_creating_info(external_id):
        idx = 0
        try:
            idx = DB.get_last_index(external_id=external_id)
        except:
            pass
        cur.execute(
            f'delete from info where external_id = {external_id} and isFinished=0'
        )
        db.commit()

    def get_info_by_id(id):
        res = cur.execute(
            f'select info.id,info.credit, info.expired_payment,info.is_official_salary,info.marital_status,info.hasCar,info.hasEstate,user.phone,user.username from info inner join user on info.external_id=user.external_id where info.id= {id}'
        )
        el = res.fetchone()
        m = ''
        m += f'Заказ №{el[0]}\n'
        m += f'Долг : {el[1]}\n'
        m += f'Есть ли просроченные платежи : {el[2]}\n'
        m += f'Доход : {el[3]}\n'
        m += f'Семейное положение : {el[4]}\n'
        m += f'Автомобиль: {el[5]}\n'
        m += f'Недвижимость: {el[6]}\n'
        m += f'Телефон: {el[7]}\n'
        m += f'Ник: @{el[8]}'

        return m

    def get_all_infos():
        res = cur.execute(
            f'select info.id,info.credit, info.expired_payment,info.is_official_salary,info.marital_status,info.hasCar,info.hasEstate,user.phone,user.username from info inner join user on info.external_id=user.external_id where isFinished=1'
        )
        data = res.fetchall()
        m = 'Данные по пользователям:'
        for el in data:
            m += '\n'
            m += f'Заказ №{el[0]}\n'
            m += f'Долг : {el[1]}\n'
            m += f'Есть ли просроченные платежи : {el[2]}\n'
            m += f'Доход : {el[3]}\n'
            m += f'Семейное положение : {el[4]}\n'
            m += f'Автомобиль: {el[5]}\n'
            m += f'Недвижимость: {el[6]}\n'
            m += f'Телефон: {el[7]}\n'
            m += f'Ник: @{el[8]}\n'
            m += '_' * 20
        return m

    def get_contacts_by_id(external_id):
        res = cur.execute(
            f'select u.real_name,u.username,u.phone from user u inner join info i on i.external_id=u.external_id  where u.external_id={external_id}'
        )

        el = res.fetchone()
        m = ''
        m += f'Имя: {el[0]}\n'
        m += f'Ник : @{el[1]}\n'
        m += f'Телефон : {el[2]}'
        return m
    
    def delete_creating_infos():
        cur.execute(
            f'delete from info where isFinished=0')
        db.commit()

    # ww admins
    def check_admin(external_id):
        res = cur.execute(
            f'select*from admin where external_id = "{external_id}" ')
        data = res.fetchone()
        if data is None:
            return False
        return True

    def get_all_admins():
        admins = []
        res = cur.execute(f'select external_id from admin')
        for id in res.fetchall():
            admins.append(id[0])
        return admins

    #WWW googlesheets
    def get_all_data():
        a = [[
            'id',
            'Имя',
            'Ник',
            'Телефон',
            'Долг',
            'Задолженнные платежи',
            'Зраплата',
            'Статус',
            'Автомобиль',
            'Недвижимость',
        ]]
        res = cur.execute(
            'select i.id, u.real_name,u.username, u.phone,i.credit,i.expired_payment,i.is_official_salary,i.marital_status,i.hasCar,i.hasEstate from info i inner join user u on i.external_id=u.external_id'
        )
        el = res.fetchall()
        for i in el:
            a.append(list(i))
        return a