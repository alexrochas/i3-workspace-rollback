import i3ipc

WORKSPACE_STACK = []
WORKSPACE_STACK_SIZE = 0


def is_debug():
    return False


def set_workspace_stack_size(size):
    global WORKSPACE_STACK_SIZE
    WORKSPACE_STACK_SIZE = size


# Define a callback to be called when you switch workspaces.
def on_workspace_focus(i3, e):
    if len(WORKSPACE_STACK) < WORKSPACE_STACK_SIZE:
        pass
    elif len(WORKSPACE_STACK) >= WORKSPACE_STACK_SIZE:
        WORKSPACE_STACK.append(e.old)
    set_workspace_stack_size(len(WORKSPACE_STACK))
    if is_debug():
        print([wspace.name for wspace in WORKSPACE_STACK])


def on_keys(i3, e):
    if e.binding.symbol == 'z' and 'Mod4' in e.binding.mods and WORKSPACE_STACK:
        if is_debug():
            print([wspace.name for wspace in WORKSPACE_STACK])
        if len(WORKSPACE_STACK) > 0:
            if is_debug():
                print('Rollback to workspace %s' % WORKSPACE_STACK[-1].name)
            i3.command('workspace %s' % WORKSPACE_STACK.pop().name)


def start():
    # Create the Connection object that can be used to send commands and subscribe
    # to events.
    i3 = i3ipc.Connection()
    # Subscribe to events
    i3.on('workspace::focus', on_workspace_focus)
    i3.on('binding', on_keys)

    # Start the main loop and wait for events to come in.
    i3.main()


if __name__ == '__main__':
    start()
