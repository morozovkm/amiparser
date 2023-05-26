from shared_func import get_config_data, connect_to_ast


def parse_ami_action(action_lines, ast_events):
    event_list = action_lines.splitlines()
    try:
        event_name = ((event_list[0]).split(': '))[1]
        if event_name in ast_events:
            CALLERID_NAME, CALLERID_NUM, EXTEN = event_handler(event_list, event_name)
        return CALLERID_NAME, CALLERID_NUM, EXTEN, event_name
    except:
        return None, None, None, None


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
