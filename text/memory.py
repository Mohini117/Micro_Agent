from message import Message


def create_memory():
    history = []

    def add_message(message):
        history.append(message)

    def get_history():
        return history

    return add_message, get_history


if __name__ == "__main__":
    add_message, get_history = create_memory()

    add_message(Message("user", "What does this medicine do?"))
    add_message(Message("assistant", "It's for blood pressure."))

    history = get_history()
    print(len(history))
    print(history[0].content)
