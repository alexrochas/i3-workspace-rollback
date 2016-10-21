import unittest
from contextlib import contextmanager

import rollback
from unittest.mock import MagicMock


@contextmanager
def rollback_event():
    mocked_event = MagicMock()
    mocked_event.binding.symbol = 'z'
    mocked_event.binding.mods = ['Mod4']
    mocked_i3 = MagicMock()
    yield mocked_i3, mocked_event
    rollback.on_keys(mocked_i3, mocked_event)  # every time a rollback is invoked, workspace_focus is triggered
    rollback.on_workspace_focus(mocked_i3, mocked_event)


@contextmanager
def workspace_focus_event():
    mocked_event = MagicMock()
    mocked_event.binding.symbol = 'z'
    mocked_event.binding.mods = ['Mod4']
    mocked_i3 = MagicMock()
    yield mocked_i3, mocked_event
    rollback.on_workspace_focus(mocked_i3, mocked_event)


class TestRollback(unittest.TestCase):
    def test_should_call_workspace_change_on_right_key_binding(self):
        with rollback_event() as (i3, event):
            mocked_worspace = MagicMock()
            mocked_worspace.name = 'random name'
            rollback.set_workspace_stack_size(0)
            rollback.WORKSPACE_STACK = [mocked_worspace]

        i3.command.assert_called_with('workspace random name')

    def test_should_on_workspace_change_add_old_workspace_to_stack(self):
        with workspace_focus_event() as (i3, event):
            mocked_worspace = MagicMock()
            mocked_worspace.name = 'random name'
            rollback.WORKSPACE_STACK = []
            rollback.set_workspace_stack_size(0)
            event = MagicMock()
            event.binding.symbol = 'z'
            event.binding.mods = ['Mod4']
            event.old = mocked_worspace

        self.assertEqual(len(rollback.WORKSPACE_STACK), 1)

    def test_should_rollback_one_workspace(self):
        with rollback_event() as (i3, event):
            mocked_worspace1 = MagicMock()
            mocked_worspace1.name = 'random name 1'
            mocked_worspace2 = MagicMock()
            mocked_worspace2.name = 'random name 2'
            mocked_worspace3 = MagicMock()
            mocked_worspace3.name = 'random name 3'
            mocked_worspace4 = MagicMock()
            mocked_worspace4.name = 'random name 4'
            rollback.WORKSPACE_STACK = [mocked_worspace1, mocked_worspace2, mocked_worspace3, mocked_worspace4]
            rollback.set_workspace_stack_size(4)

        self.assertEqual(len(rollback.WORKSPACE_STACK), 3)
