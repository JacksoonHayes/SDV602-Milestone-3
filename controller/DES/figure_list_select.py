"""
figure list controller
"""
import sys
sys.dont_write_bytecode = True

def accept(event, values, state):
    """
    Accepts an event, values, and state as parameters.
    Calls the 'figure_list_draw' method of the 'view' object in the state, passing the values.
    Returns True.
    """
    view = state['view']
    view.figure_list_draw(values)
    return True

