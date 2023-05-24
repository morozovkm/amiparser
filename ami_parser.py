import telnetlib
import configparser


def get_config_data():
    config = configparser.ConfigParser()
    config.read('ami_parser.conf')
    ast_ip = config.get('general', 'asterisk_ip')
    ast_port = config.get('general', 'asterisk_ami_port')
    ast_events = config.get('general', 'events')
    ast_events = ast_events.split(',')
    return ast_ip, ast_port, ast_events


def connect_to_ast(ast_ip, ast_port):
    tc = telnetlib.Telnet(host=ast_ip, port=ast_port)
    tc.read_until(b'Asterisk Call Manager/5.0.5')
    tc.write(b'Action: Login\n')
    tc.write(b'Username: amiuser\n')
    tc.write(b'Secret: 123456\n')
    tc.write(b'\n')
    tc.write(b'\n')
    tc.read_until(b'Message: Authentication accepted')
    return tc


def parse_ami_action(action_lines, ast_events):
    event_list = action_lines.splitlines()
    try:
        event_name = ((event_list[0]).split(': '))[1]
        if event_name in ast_events:
            CALLERID_NAME, CALLERID_NUM, EXTEN = event_handler(event_list, event_name)
        return CALLERID_NAME, CALLERID_NUM, EXTEN, event_name
    except:
        return None,None,None,None

def event_handler(event_list, event_name):
    CALLERID_NAME = None
    CALLERID_NUM = None
    EXTEN = None
    if event_name == 'DialBegin':
        CALLERID_NUM = ((event_list[5]).split(': '))[1]
        CALLERID_NAME = ((event_list[6]).split(': '))[1]
        EXTEN = ((event_list[12]).split(': '))[1]
    elif event_name == 'BridgeEnter':
        CALLERID_NUM = ((event_list[13]).split(': '))[1]
        CALLERID_NAME = ((event_list[14]).split(': '))[1]
        EXTEN = ((event_list[19]).split(': '))[1]
    elif event_name == 'Hangup':
        CALLERID_NUM = ((event_list[5]).split(': '))[1]
        CALLERID_NAME = ((event_list[6]).split(': '))[1]
        EXTEN = ((event_list[12]).split(': '))[1]
    else:
        pass
    return CALLERID_NAME, CALLERID_NUM, EXTEN


if __name__ == '__main__':
    ast_ip, ast_port, ast_events = get_config_data()
    tc = connect_to_ast(ast_ip, ast_port)

    while True:
        data = tc.read_until(b'\n\r\n')
        CALLERID_NAME, CALLERID_NUM, EXTEN, event_name = parse_ami_action(data.decode(), ast_events)
        if CALLERID_NUM:
            print(CALLERID_NAME, CALLERID_NUM, EXTEN, event_name)
