import traceback
import os

def format_error(error: Exception):
    tb_info = traceback.extract_tb(error.__traceback__)
    error_messge = '<b><code>'+ type(error).__name__ + '</b>: ' + str(error)+'<code><br>'
    for tb in tb_info:
        filename, lineno, func, text = tb
        error_messge += '<code><b>%s:%i</b>] %s(): %s</code><br>'%(os.path.basename(filename), lineno, func, text)
    return error_messge
