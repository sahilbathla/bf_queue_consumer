from kafka import KafkaConsumer
import time
import thread
import atexit

BOOTSTRAP_SERVERS = ['localhost:9092']
RETRIES = 3

class BaseConsumer(object):

    def __init__(self, topic):
        self.topic = topic
        self.consumer = KafkaConsumer(topic, bootstrap_servers=BOOTSTRAP_SERVERS)
        self.shutdown = False
        atexit.register(self.shutdown_event)

    def add_to_failsafe(self, msg):
        try:
           thread.start_new_thread( self.handle_failed_msg, (msg,) )
        except:
           print "Error: unable to start thread"

    def run(self):
        try:
            while True:
                print "Fetching messages for %s" %self.topic
                messages = self.consumer.poll(timeout_ms=100)
                if messages:
                    for msgs in list(messages.values()):
                        for msg in msgs:
                            print "Message received for %s" %self.topic
                            try:
                                self.handle(msg)
                            except Exception as e:
                                print "Message could not handled pushing to failsafe"
                                self.add_to_failsafe(msg)

                time.sleep(1)
        except KeyboardInterrupt:
            self.shutdown_event()
        except Exception as e:
            print format(e)

    def handle_failed_msg(self, msg):
        i = 0
        success = False
        while i < RETRIES:
            i += 1
            try:
                self.handle(msg)
                success = True
                print "Failed message was executed successfuly"
                break
            except Exception as e:
                pass
        if not success:
            print "Failed message was not executed successfuly"
            #send a email to inform devs
            pass


    def handle(self, msg):
        True
        #override in child consumers

    def shutdown_event(self):
        if self.shutdown == False:
            self.handle_shutdown()
        self.shutdown = True

    def handle_shutdown(self):
        print "Shutting down consumer for %s" %self.topic
        #Override to handle specific shutdown cases