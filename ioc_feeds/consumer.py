from kafka import KafkaConsumer
from json import loads

class KafkaConsumerWrapper(object):

    __instance = None

    def __init__(self) -> None:
        raise RuntimeError("Use instance() instead")

    @classmethod
    def json_deserializer(self, data):
        return loads(data)

    @classmethod
    def instance(cls):
        if cls.__instance is None:
            cls.__instance = KafkaConsumer(
                "ioc_feed",
                bootstrap_servers=[
                    "localhost:9092"
                ],
                value_deserializer=cls.json_deserializer
            )
        return cls.__instance