"""
Uploader button controller
"""
import sys
sys.dont_write_bytecode = True

def accept( event, values, state):
    from view.update_file_view import UpdateView
    
    keep_going = True
    if event == 'Upload CSV':
        des_obj = UpdateView()
        des_obj.explorer_view = state['view']
        des_obj.explorer_values = values
        des_obj.set_up_layout()
        des_obj.render()
        des_obj.accept_input()
    return keep_going 