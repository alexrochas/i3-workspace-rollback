import unittest
import rollback
from unittest.mock import MagicMock


class TestRollback(unittest.TestCase):
    def test_should_call_workspace_change_on_right_key_binding(self):
        mocked_worspace = MagicMock()
        mocked_worspace.name = 'random name'
        rollback.WORKSPACE_STACK = [mocked_worspace]
        mocked_event = MagicMock()
        mocked_event.binding.symbol = 'z'
        mocked_event.binding.mods = ['Mod4']
        mocked_i3 = MagicMock()

        rollback.on_keys(mocked_i3, mocked_event)

        mocked_i3.command.assert_called_with('workspace random name')

    def test_should_on_workspace_change_add_old_workspace_to_stack(self):
        mocked_worspace = MagicMock()
        mocked_worspace.name = 'random name'
        rollback.WORKSPACE_STACK = []
        mocked_event = MagicMock()
        mocked_event.binding.symbol = 'z'
        mocked_event.binding.mods = ['Mod4']
        mocked_event.old = mocked_worspace
        mocked_event.current = mocked_worspace
        mocked_i3 = MagicMock()

        rollback.on_workspace_focus(mocked_i3, mocked_event)

        self.assertEqual(len(rollback.WORKSPACE_STACK), 2)
