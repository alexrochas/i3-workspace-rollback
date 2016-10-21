import i3ipc

WORKSPACE_STACK = []


# Define a callback to be called when you switch workspaces.
def on_workspace_focus(i3, e):
    if len(WORKSPACE_STACK) == 0:
        WORKSPACE_STACK.append(e.old)
        WORKSPACE_STACK.append(e.current)
    if e.current and e.old:
        if e.current.name == e.old.name:
            return
        elif e.current.name == WORKSPACE_STACK[-1].name:
            return
        else:
            WORKSPACE_STACK.append(e.current)
    print([wspace.name for wspace in WORKSPACE_STACK])


def on_keys(i3, e):
    if e.binding.symbol == 'z' and 'Mod4' in e.binding.mods and WORKSPACE_STACK:
        print([wspace.name for wspace in WORKSPACE_STACK])
        if WORKSPACE_STACK and len(WORKSPACE_STACK) == 1:
            i3.command('workspace %s' % WORKSPACE_STACK[0].name)
            return
        elif WORKSPACE_STACK:
            WORKSPACE_STACK.pop()  # FIXME workaround
            print('Rollback to workspace %s' % WORKSPACE_STACK[-1].name)
            i3.command('workspace %s' % WORKSPACE_STACK.pop().name)


if __name__ == '__main__':
    # Create the Connection object that can be used to send commands and subscribe
    # to events.
    i3 = i3ipc.Connection()
    # Subscribe to events
    i3.on('workspace::focus', on_workspace_focus)
    i3.on('binding', on_keys)

    # Start the main loop and wait for events to come in.
    i3.main()
