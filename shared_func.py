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
