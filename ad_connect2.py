from ldap3 import Server, Connection, SASL, DIGEST_MD5, SUBTREE, NTLM, ALL

##import ldap3 as ldap
##from ldap3 import Connection, Server, SIMPLE, SYNC, SUBTREE, ALL

server = Server(host='10.10.103.208', port=389, get_info=ALL)
conn = Connection(server, auto_bind=True, version=3, client_strategy='SYNC', authentication=NTLM,
                  user='aster.local\Kostya', password='123Qaz!')
print('test')
#print(server.info)
print(conn.bind())
print('test2')

user_dn = "dc=aster,dc=local"
base_dn = "dc=aster,dc=local"
filter = "uid=admin"
total_entries = 0
result = conn.search(search_base='CN=Users,DC=aster,DC=local', search_filter = "(objectClass=Person)", search_scope=SUBTREE, attributes = ['telephoneNumber','name'])
# total_entries += len(conn.response)
#result = conn.search(search_base=base_dn, search_scope=SUBTREE)
# logger.info('SEARCHING COMPLETE') #does not appear in the log
# return all user data results
# for entry in conn.response:
#    print(entry)
##print(entry['dn'], entry['attributes'])
print(result)
print('------------------------------------------------------------------------------------')
#print(conn.response)
user_list = conn.entries
user_dict = {}
for user in user_list:
    #print(user)
    #print(type(user))
    #print(user['telephoneNumber'], user['name'])
    user_dict[str(user['name'])] = str(user['telephoneNumber'])
print('------------------------------------------------------------------------------------')

print(user_dict)
conn.unbind()
