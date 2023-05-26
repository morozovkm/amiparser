from shared_func import get_config_data, connect_to_ast
import argparse


def call_to(tc, CALLERID, EXTEN):
    CH_STR = bytes('Channel: SIP/{}\n'.format(CALLERID), 'utf-8')
    EXT_STR = bytes('Exten: {}\n'.format(EXTEN), 'utf-8')
    CID_STR = bytes('Callerid: {}\n'.format(CALLERID), 'utf-8')
    tc.write(b'\n')
    tc.write(b'Action: Originate\n')
    tc.write(CH_STR)
    tc.write(b'Context: my\n')
    tc.write(EXT_STR)
    tc.write(b'Priority: 1\n')
    tc.write(CID_STR)
    tc.write(b'\n')
    tc.write(b'\n')


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('CALLERID', help="Calling PN")
    parser.add_argument('EXTEN', help="Called PN")
    args = parser.parse_args()
    return args.CALLERID, args.EXTEN


if __name__ == '__main__':
    ast_ip, ast_port, ast_events = get_config_data()
    tc = connect_to_ast(ast_ip, ast_port)
    CALLERID, EXTEN = parse_args()
    call_to(tc, CALLERID, EXTEN)
