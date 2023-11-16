"""
figure list controller
"""
import sys
sys.dont_write_bytecode = True

def accept( event, values, state):
    view = state['view']
    view.figure_list_draw(values)
    return True


