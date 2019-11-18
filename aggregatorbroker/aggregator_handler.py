import json
import logging
import threading
from datetime import datetime, timedelta
from time import sleep

import pandas as pd

import utils
from constants import *
from sql_writer import SqlWriter


class MessageHandler:
    """
    Class that handles messages received using a message broker
    """

    def handle_message(self, ts_reception: datetime, message_str: str):
        """
        Handle a message for a message broker
        :param ts_reception: the time this message was received
        :param message_str: the message payload (json string)
        """
        pass


class AggregatorHandler(MessageHandler):

    def __init__(self, sql_writer: SqlWriter, mqtt_delay: int = 1):
        self.sql_writer = sql_writer
        self.mqtt_delay = timedelta(seconds=mqtt_delay)
        self.messages = {}
        self.previous_minute = utils.extract_datetime_minute(utils.now())
        # create a thread that will aggregate messages each minutes and write them to the data base
        agg_thread = threading.Thread(target=self._aggregate_messages)  # instantiating without any argument
        agg_thread.start()

    def _aggregate_messages(self):
        # first time we need to wait to the end of the first minute
        self._sleep(utils.next_minute(self.previous_minute))
        while True:
            if self.previous_minute in self.messages:
                # retrieve the message for the previous minute
                msg_minute = self.messages.pop(self.previous_minute)

                # aggregate messages and write them to the database
                self._aggregate_and_write(self.previous_minute, msg_minute)

            self.previous_minute = utils.next_minute(self.previous_minute)
            self._sleep(self.previous_minute)

    def _aggregate_and_write(self, ts_minute: datetime, msg_minute: list):
        """
        Method that aggregate messages and write them to the database
        :param msg_minute: the messages to aggregate
        """
        logging.info("Aggregate data of {} and write in the database".format(str(ts_minute)))
        df = pd.DataFrame(msg_minute, columns=[MACHINE, TS, LOAD_RATE, MILEAGE])
        mean_grpby = df.groupby([MACHINE]).mean()
        mean_grpby.insert(0, TS, ts_minute)
        self.sql_writer.write(mean_grpby)

    def _sleep(self, next_minute: datetime):
        """
        Sleep until the next minute to handle with a delay to handle messages received by the mqtt broker
        :param next_minute the next minute until it sleep
        """
        sleep_duration = (next_minute - utils.now() + self.mqtt_delay).total_seconds()
        # sleep only if we have time. The processing of previous message could potentially takes more than one minute
        if sleep_duration > 0:
            logging.info("Sleep for {} seconds before next aggregation {}".format(
                sleep_duration,
                next_minute + self.mqtt_delay))
            sleep(sleep_duration)

    def handle_message(self, ts_reception: datetime, message_str: str):
        """
        Handle a message and add it to the set of messages to aggregate
        :param ts_reception: the time this message was received
        :param message_str: the message payload (json string)
        """
        message = json.loads(message_str)

        p_message = self._process_message(ts_reception, message)
        if p_message is not None:
            minute = utils.extract_datetime_minute(p_message[1])
            if minute not in self.messages:
                self.messages[minute] = []
            self.messages.get(minute).append(p_message)

    def _process_message(self, ts_reception, message):
        """
        process the message and return the processed message or null if the message is not coherent and should not be
        processed
        :param ts_reception: the reception date time of the message
        :param message: the raw message
        :return: the processed message
        """
        ts = utils.parse_datetime(message[TS])  # transform to a datetime
        # we do not take into account messages where the timestamp is in the future
        # we only handle past messages with a delay of 1 seconds
        if ts_reception >= ts:
            # TODO here we should check message integrity (see NOTES.md)
            machine = int(message[MACHINE])
            load_rate = float(message[LOAD_RATE])
            mileage = float(message[MILEAGE])
            return [machine, ts, load_rate, mileage]
        logging.debug("The message {} has not been processed due to integrity error ".format(message))
