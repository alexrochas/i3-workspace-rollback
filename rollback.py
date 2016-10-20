import i3ipc

# Create the Connection object that can be used to send commands and subscribe
# to events.
i3 = i3ipc.Connection()
workspace_stack = []


# Define a callback to be called when you switch workspaces.
def on_workspace_focus(i3, e):
    if len(workspace_stack) == 0:
        workspace_stack.append(e.old)
        workspace_stack.append(e.current)
    if e.current and e.old:
        if e.current.name == e.old.name:
            return
        elif e.current.name == workspace_stack[-1].name:
            return
        else:
            workspace_stack.append(e.current)
    print([wspace.name for wspace in workspace_stack])


def on_keys(i3, e):
    if e.binding.symbol == 'z' and 'Mod4' in e.binding.mods and workspace_stack:
        print([wspace.name for wspace in workspace_stack])
        if workspace_stack and len(workspace_stack) == 1:
            i3.command('workspace %s' % workspace_stack[0].name)
            return
        elif workspace_stack:
            workspace_stack.pop()  # FIXME workaround
            print('Rollback to workspace %s' % workspace_stack[-1].name)
            i3.command('workspace %s' % workspace_stack.pop().name)


# Subscribe to events
i3.on('workspace::focus', on_workspace_focus)
i3.on('binding', on_keys)

# Start the main loop and wait for events to come in.
i3.main()
