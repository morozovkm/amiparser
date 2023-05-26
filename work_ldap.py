from ldap3 import Server, Connection, SASL, DIGEST_MD5, SUBTREE, NTLM, ALL
import pymysql
import random


def get_data_from_ldap(host, port, user, password, seach_base):
    server = Server(host=host, port=port, get_info=ALL)
    conn = Connection(server, auto_bind=True, version=3, client_strategy='SYNC', authentication=NTLM,
                      user=user, password=password)
    user_dn = "dc=aster,dc=local"
    base_dn = "dc=aster,dc=local"
    filter = "uid=admin"
    total_entries = 0
    result = conn.search(search_base=seach_base, search_filter="(objectClass=Person)",
                         search_scope=SUBTREE, attributes=['telephoneNumber', 'name'])
    user_list = conn.entries
    user_dict = {}
    for user in user_list:
        user_dict[str(user['name'])] = str(user['telephoneNumber'])
    conn.unbind()
    return user_dict


if __name__ == '__main__':
    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    host = '10.10.103.208'
    port = 389
    user = 'aster.local\Kostya'
    password = '123Qaz!'
    seach_base = 'CN=Users,DC=aster,DC=local'
    user_dict = get_data_from_ldap(host, port, user, password, seach_base)
    print('!!!!!!!!!!!!!!!!!!!')
    print(user_dict)

    m_conn = pymysql.connect(host='10.10.103.233', port = 3306, user='ldap', password='123456', database='testast')
    cursor = m_conn.cursor()
    for element in user_dict:
        print(element)
        print(user_dict[element])
        if user_dict[element] != '[]':
            select_line = f'select count(*) from sip where name = "{element}"'
            cursor.execute(select_line)
            result = int(cursor.fetchall()[0][0])
            print(result)
            if result == 0:
                for n in range(len(chars)):
                    passwd = ''
                    for i in range(6):
                        passwd += random.choice(chars)

                print(passwd)
                sql_line = f'insert into sip values ("{element}","{passwd}","{user_dict[element]}")'
                cursor.execute(sql_line)
    m_conn.commit()


