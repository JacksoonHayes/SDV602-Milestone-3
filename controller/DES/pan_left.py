"""
Pan Left button controller
"""
import PySimpleGUI as sg
# Import other necessary modules...

def accept(event, values, state):
    keep_going = True

    if event == '<':  # Replace '<' with your specific event for panning left
        try:
            # Use the existing axis from the state if available
            axis = state.get('axis')
            if axis:
                factor = 0.2  # The factor by which to pan left

                # Get the current x-axis limits
                xmin, xmax = axis.get_xlim()

                # Calculate new x-axis limits to pan left
                new_xmin = xmin - factor
                new_xmax = xmax - factor

                # Set the new x-axis limits
                axis.set_xlim(new_xmin, new_xmax)

                # Update the canvas after panning
                canvas = state.get('canvas')
                if canvas:  # If there's a canvas key in state, use it to draw
                    canvas.draw()

        except Exception as e:
            sg.PopupError('An error occurred while panning left:', e)
            keep_going = False  # Stop the event loop if there's an error

    return keep_going
