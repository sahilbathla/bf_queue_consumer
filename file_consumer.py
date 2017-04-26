from base_consumer import BaseConsumer

TOPIC = 'buffer'

class FileConsumer(BaseConsumer):
    def __init__(self):
        super(FileConsumer, self).__init__(TOPIC)

    def handle(self, msg):
        file = open('dumpfile', 'a')
        file.write(msg.value)
        file.close()