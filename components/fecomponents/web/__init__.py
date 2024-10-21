import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

def get(component):
    if component == 'container':
        import container
        return container.Container
    elif component == 'edit':
        import edit
        return edit.Edit
    elif component == 'button':
        import button
        return button.Button
    elif component == 'tableview':
        import tableview
        return tableview.TableView