from drivers.fake_apa102 import APA102
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from multiprocessing import Process
import json
import mqtt.helpers as helpers
from mqtt.helpers import TopicAspect
import logging as log

# global handles
conf = None  # the user config
show_process = Process()  # for the process in which the lightshows run in
strip = None  # for the APA102 LED strip


# send to the MQTT notification channel: Node-RED will display a toast notification
def notify_user(message, qos=0):
    publish.single(
        topic=conf.mqtt.notification_path.format(prefix=conf.mqtt.prefix, sys_name=conf.sys_name),
        payload=message,
        qos=qos,
        hostname=conf.mqtt.broker.host,
        port=conf.mqtt.broker.port,
        keepalive=conf.mqtt.broker.keepalive
    )


# subscribe to all messages related to this LED installation
def on_connect(client, userdata, flags, rc):
    subscription_path = helpers.assemble_path(show_name="+", command="+")
    client.subscribe(subscription_path)
    log.info("subscription on broker {host} for {path}".format(host=conf.mqtt.broker.host, path=subscription_path))


def on_message(client, userdata, msg):
    # store parameters as strings
    topic = str(msg.topic)
    if type(msg.payload) is bytes:  # might be a byte encoded string that must be stripped
        payload = helpers.binary_to_string(msg.payload)
    else:
        payload = str(msg.payload)

    # extract the essentials
    show_name = helpers.get_from_topic(TopicAspect.show_name.value, topic)
    command = helpers.get_from_topic(TopicAspect.command.value, topic)

    # check if this is a relevant command for us
    supported_commands = ["start", "stop"]
    if command not in supported_commands:
        log.debug("MQTTControl ignored {show}:{command}".format(show=show_name, command=command))
        return

    # parse parameters
    parameters = helpers.parse_json_safely(payload)
    log.debug(
        """for show: \"{show}\":
           received command: \"{command}\"
           with:
           {parameters}
        """.format(show=show_name,
                   command=command,
                   parameters=json.dumps(parameters, sort_keys=True, indent=8, separators=(',', ': '))
                   ))

    # execute
    if command == "start":
        # stop the running show
        stop_running_show()
        start_show(show_name, parameters)
    elif command == "stop":
        stop_show(show_name)


def start_show(show_name: str, parameters: dict):
    global conf

    # search for show module
    if show_name in conf.shows:
        show = conf.shows[show_name]
    else:
        log.warning("Show {name} was not found!".format(name=show_name))
        return

    # check for valid parameters
    if not show.parameters_valid(parameters):
        log.warning("invalid parameters sent!")
        return

    log.info("Starting the show " + show_name)
    global show_process, strip
    arguments = {"strip": strip, "conf": conf, "parameters": parameters}
    show_process = Process(target=show.run, name=show_name, kwargs=arguments)
    show_process.start()


def stop_show(show_name: str):
    if show_name is show_process.name or show_name is "all":
        stop_running_show()
        return


def stop_running_show(timeout_sec: int = 5):
    global show_process, strip

    if show_process.is_alive():
        show_process.join(timeout_sec)
        log.info("{show_name} is running. Terminating...".format(show_name=show_process.name))
    else:
        log.info("no show running; all good")

    strip.clearBuffer()  # just in case


def run(config) -> None:
    global conf, show_process, strip

    log.getLogger().setLevel(log.DEBUG)

    # store config
    conf = config

    log.info("Starting {name}".format(name=conf.sys_name))

    log.info("Initializing LED strip...")
    strip = APA102(conf.strip.num_leds, conf.strip.global_brightness, 'rgb', conf.strip.max_spi_speed_hz)
    strip.verbose = False  # @nopi

    log.info("Connecting to the MQTT broker")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(conf.mqtt.broker.host, conf.mqtt.broker.port, conf.mqtt.broker.keepalive)
    log.info("{name} is ready".format(name=conf.sys_name))

    client.loop_forever()
    log.critical("MQTTControl.py has exited")
