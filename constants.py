import os

MONGO_URI = f'mongodb+srv://{os.getenv("MONGO_USER")}:{os.getenv("MONGO_PASS")}@cluster0.1xhpwlb.mongodb.net/?retryWrites=true&w=majority'
BROKER_URI = f'amqp://{os.getenv("RABBITMQ_USER")}:{os.getenv("RABBITMQ_PASS")}@rabbitmq:5672'
