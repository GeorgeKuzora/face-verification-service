from app.external.kafka import KafkaConsumer


def test_consumer(service):
    consumer = KafkaConsumer(service)
