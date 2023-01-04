from kafka import KafkaProducer
from json import dumps


class KafkaProducerWrapper(object):
    __instance = None

    def __init__(self) -> None:
        raise RuntimeError("Use instance() instead")

    @classmethod
    def instance(self):
        if self.__instance is None:
            self.__instance = KafkaProducer(
                # TODO: ADD CONFIGURATION THRU DJANGO!!
                bootstrap_servers=[
                    "localhost:9092"
                ],
                value_serializer=lambda data: dumps(data).encode('utf-8')
            )
        return self.__instance
