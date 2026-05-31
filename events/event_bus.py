class EventBus:
    _listeners = {}

    @classmethod
    def subscribe(cls, event, handler):
        cls._listeners.setdefault(event, []).append(handler)

    @classmethod
    def publish(cls, event, data):
        for h in cls._listeners.get(event, []):
            h(data)