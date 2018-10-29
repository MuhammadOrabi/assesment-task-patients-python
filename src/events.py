import pika
import json

credentials = pika.PlainCredentials('rabbitmq', 'rabbitmq')
consumer = pika.BlockingConnection(pika.ConnectionParameters('rabbit1', 5672, '/', credentials))
publisher = pika.BlockingConnection(pika.ConnectionParameters('rabbit1', 5672, '/', credentials))

def run_all():
    send_data({'message': 'hello, world!'})
    get_data()



def send_data(data):
    channel = publisher.channel()
    exchange_name = 'user_updates'
    routing_key   = 'user.profile.update'

    # This will create the exchange if it doesn't already exist.
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=True)

    channel.basic_publish(exchange=exchange_name,
                          routing_key=routing_key,
                          body=json.dumps(data),
                          # Delivery mode 2 makes the broker save the message to disk.
                          # This will ensure that the message be restored on reboot even  
                          # if RabbitMQ crashes before having forwarded the message.
                          properties=pika.BasicProperties(
                            delivery_mode = 2,
                        ))
    print("%r sent to exchange %r with data: %r" % (routing_key, exchange_name, data))
    publisher.close()



def get_data():
    channel = consumer.channel()
    print(" [x] Getting data")

    exchange_name = 'user_updates'
    routing_key   = 'user.profile.update'
    channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=True)
    result = channel.queue_declare(exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)

    method_frame, header_frame, body = channel.basic_get(queue_name)
    if method_frame:
        print(method_frame, header_frame, body)
    else:
        print('No message returned')