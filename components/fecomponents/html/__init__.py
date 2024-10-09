def get(component):
    # Container hat nur Styles
    if component == 'container':
        import container
        return container.Container
    # dynamische Komponenten haben HTML und Styles
    elif component == 'edit':
        import edit
        return edit.Edit
    elif component == 'button':
        import button
        return button.Button