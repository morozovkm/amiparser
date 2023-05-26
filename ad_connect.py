#import ldap3
from ldap3 import Server, Connection, SUBTREE


AD_SERVER = '10.10.103.208'
AD_USER = 'aster.local\Администратор'
AD_PASSWORD = '123Qaz'
AD_SEARCH_TREE = 'dc=aster, dc=local'

#соединяюсь с сервером. всё ОК
server = Server(AD_SERVER)
conn = Connection(server, user=AD_USER, password=AD_PASSWORD)
conn.bind()

