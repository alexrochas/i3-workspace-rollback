import i3
import pickle


def persist_to_file(content, filename='./mock/event/state.data'):
    with open(filename, 'wb') as f:
        pickle.dump(content, f)


def read_from_file(filename='./mock/event/state.data'):
    with open(filename, 'rb') as f:
        return pickle.load(f)


def rollback_callback(event, data, subscription):
    pass


subscription = i3.Subscription(rollback_callback, 'workspace')
