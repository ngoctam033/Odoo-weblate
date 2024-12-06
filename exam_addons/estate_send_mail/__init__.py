from . import models
from . import mail_server_config

def post_init_hook(cr, registry):
    mail_server_config.configure_mail_server(cr, registry)