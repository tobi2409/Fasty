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