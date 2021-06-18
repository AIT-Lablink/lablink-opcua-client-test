from opcua import ua, Server
from opcua.server.user_manager import UserManager
import code

# User database.
users_db = {
    'LablinkTestUser': 'zQC37UiH6ou',
}

# Callback function for user access management.
def user_manager(isession, username, password):
    isession.user = UserManager.User
    login_ok = username in users_db and password == users_db[username]
    print('Login attempt with username "{}": {}'.format(username, 'SUCCESS' if login_ok else 'FAILED'))
    return login_ok

# Main routine.
if __name__ == '__main__':

    server = Server()

    server.set_server_name('Lablink Test Server')
    server.set_endpoint('opc.tcp://localhost:12345/lablink-test')

    server.set_security_policy([ua.SecurityPolicyType.NoSecurity])

    server.set_security_IDs(['Username'])
    server.user_manager.set_user_manager(user_manager)

    idx = server.register_namespace('urn:lablink:opcua-test')

    folder_lablink_test = server.nodes.objects.add_folder(idx, 'LablinkTestSetup')

    str_nodeid_stub = 'ns={};s=LablinkTestSetup/{};'
    
    str_nodeid = str_nodeid_stub.format(idx, 'Variable1_Double')
    var = folder_lablink_test.add_variable(str_nodeid, 'Variable1_Double', 0, ua.VariantType.Double)
    var.set_writable()
        
    str_nodeid = str_nodeid_stub.format(idx, 'Variable2_Int64')
    var = folder_lablink_test.add_variable(str_nodeid, 'Variable2_Int64', 0, ua.VariantType.Int64)
    var.set_writable()        

    server.start()

    try:
        myvars = globals()
        myvars.update(locals())
        shell = code.InteractiveConsole(myvars)
        shell.interact()
    finally:
        server.stop()
