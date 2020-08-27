import logging
import os
import time
import commands
import datetime
import graphyte
import socket

from colorlog import ColoredFormatter

LOG_LEVEL = logging.DEBUG
LOGFORMAT = "%(asctime)s %(log_color)s%(levelname)-8s%(reset)s %(log_color)s%(message)s%(reset)s"

logging.root.setLevel(LOG_LEVEL)
formatter = ColoredFormatter(LOGFORMAT)
stream = logging.StreamHandler()
stream.setLevel(LOG_LEVEL)
stream.setFormatter(formatter)
log = logging.getLogger('pythonConfig')
log.setLevel(LOG_LEVEL)
log.addHandler(stream)

BetaNet_EPOCH_BLOCKS = 10000
TestNet_EPOCH_BLOCKS = 43200
MainNet_EPOCH_BLOCKS = 43200
CURRENT_NET_EPOCH_BLOCKS = TestNet_EPOCH_BLOCKS
RATE = 1000000000000000000000000
NET = 'testnet'
ACCOUNTID = 'sparkpool.testnet'
CONTRACTID = 'sparkpool.pool.6fb1358'
MONITOR_API_URL = 'http://127.0.0.1:3030'


# MONITOR_API_URL = 'https://rpc.testnet.near.org'


def get_height():
    CURRENT_HEIGHT = """curl -s {}/status | jq .sync_info.latest_block_height""".format(MONITOR_API_URL)
    CURRENT_HEIGHT = float(os.popen(CURRENT_HEIGHT).read().strip('\n'))
    EPOCH_START_HEIGHT = """curl -s -d '{"jsonrpc": "2.0", "method": "validators", "id": "dontcare", "params": [null]}' -H 'Content-Type: application/json'""" + """ {} | jq .result.epoch_start_height""".format(MONITOR_API_URL)
    EPOCH_START_HEIGHT = float(os.popen(EPOCH_START_HEIGHT).read().strip('\n'))
    HEIGHT_TO_NEXT_EPOCH = EPOCH_START_HEIGHT + CURRENT_NET_EPOCH_BLOCKS - CURRENT_HEIGHT
    EPOCH_PASSED_PERCET = float(CURRENT_HEIGHT - EPOCH_START_HEIGHT) / float(CURRENT_NET_EPOCH_BLOCKS) * 100
    log.info("near current height is {}.".format(CURRENT_HEIGHT))
    log.info("It has {} heights to next epoch.".format(HEIGHT_TO_NEXT_EPOCH))
    log.info("epoch have passed {}%.".format(EPOCH_PASSED_PERCET))
    return CURRENT_HEIGHT, HEIGHT_TO_NEXT_EPOCH, EPOCH_PASSED_PERCET


def get_seat_price():
    VALIDATOR_CURRENT_PRICE = """near validators current --nodeUrl %s | awk '/price/ {print substr($6, 1, length($6)-2)}' | sed 's/,//g'""" % (MONITOR_API_URL)
    VALIDATOR_CURRENT_PRICE = int(os.popen(VALIDATOR_CURRENT_PRICE).read().strip('\n'))
    VALIDATOR_NEXT_PRICE = """near validators next --nodeUrl %s | awk '/price/ {print substr($7, 1, length($7)-2)}' | sed 's/,//g'""" % (MONITOR_API_URL)
    VALIDATOR_NEXT_PRICE = int(os.popen(VALIDATOR_NEXT_PRICE).read().strip('\n'))
    VALIDATOR_PROPOSAL_PRICE = """near proposals --nodeUrl %s | awk '/price =/ {print substr($15, 1, length($15)-1)}' | sed 's/,//g'""" % (MONITOR_API_URL)
    VALIDATOR_PROPOSAL_PRICE = int(os.popen(VALIDATOR_PROPOSAL_PRICE).read().strip('\n'))
    log.info("validator current epoch seat price is {}.".format(VALIDATOR_CURRENT_PRICE))
    log.info("validator next epoch seat price is {}.".format(VALIDATOR_NEXT_PRICE))
    log.info("validator proposal price is {}.".format(VALIDATOR_PROPOSAL_PRICE))
    return VALIDATOR_CURRENT_PRICE, VALIDATOR_NEXT_PRICE, VALIDATOR_PROPOSAL_PRICE


def get_stake_amount():
    STAKE_AMOUNT = """near view %s get_total_staked_balance '{}' --nodeUrl %s""" % (CONTRACTID, MONITOR_API_URL)
    STAKE_AMOUNT = float(os.popen(STAKE_AMOUNT).read().strip('\n').split("\'")[1])
    ACCOUNT_TOTAL_BALANCE = """near view %s get_account_total_balance '{"account_id": "%s"}' --nodeUrl %s""" % (CONTRACTID, ACCOUNTID, MONITOR_API_URL)
    ACCOUNT_TOTAL_BALANCE = float(os.popen(ACCOUNT_TOTAL_BALANCE).read().strip('\n').split("\'")[1])
    ACCOUNT_STAKED_BALANCE = """near view %s get_account_staked_balance '{"account_id": "%s"}' --nodeUrl %s""" % (CONTRACTID, ACCOUNTID, MONITOR_API_URL)
    ACCOUNT_STAKED_BALANCE = float(os.popen(ACCOUNT_STAKED_BALANCE).read().strip('\n').split("\'")[1])
    log.info("{} stake amount is {}.".format(ACCOUNTID, STAKE_AMOUNT))
    return STAKE_AMOUNT / RATE, ACCOUNT_TOTAL_BALANCE / RATE, ACCOUNT_STAKED_BALANCE / RATE


def get_next_epoch_validator_status():
    VALIDATOR_STATUS = "near validators next --nodeUrl %s| grep %s | awk -F' ' '{print $2}'" % (MONITOR_API_URL, CONTRACTID)
    RECODE, OUTPUT = commands.getstatusoutput(VALIDATOR_STATUS)
    log.info("{} RECODE: {}, OUTPUT: {}.".format(get_next_epoch_validator_status.__name__, RECODE, OUTPUT))

    return RECODE, OUTPUT


def ping_contract(MONITOR_API_URL='https://rpc.testnet.near.org'):
    PING = """near call %s ping '{}' --accountId %s --nodeUrl %s""" % (CONTRACTID, ACCOUNTID, MONITOR_API_URL)
    RECODE, OUTPUT = commands.getstatusoutput(PING)
    log.info("{} RECODE: {}, OUTPUT: {}.".format(ping_contract.__name__, RECODE, OUTPUT))


def send_to_graphite(host, path, metric, prefix):
    graphyte.init(host, prefix=prefix)
    log.info("sending graphite data path: {}, metric: {}".format(path, metric))
    try:
        graphyte.send(path, metric)
    except Exception as e:
        log.error("{}".format(e))


def send_to_slack(color, message):
    '''color: good warning danger'''
    slack_web_hook = "https://hooks.slack.com/XXXXXXXXXXXXXXXXXXXXXXXXXX"
    near_web = "https://explorer.{}.near.org/accounts/{}".format(NET, ACCOUNTID)
    ts = time.time()
    send_message = """curl -s -X POST -H 'Content-type: application/json' --data \
    '{
        "attachments": [
            {
                "color": "%s",
                "title": "near explore web url",
                "title_link": "%s",
                "text": "%s",
                "image_url": "http://my-website.com/path/to/image.jpg",
                "thumb_url": "http://example.com/path/to/thumb.png",
                "footer": "Slack API",
                "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
                "ts": '%s'
            }
        ]
    }' %s""" % (color, near_web, message, ts, slack_web_hook)
    RECODE, OUTPUT = commands.getstatusoutput(send_message)
    log.info("{} RECODE: {}, OUTPUT: {}.".format(send_to_slack.__name__, RECODE, OUTPUT))


if __name__ == "__main__":
    ALERT_STATUS = False
    hostname = socket.gethostname()
    target_server = "graphite-url"
    metric_list = {}
    while True:
        # height
        CURRENT_HEIGHT, HEIGHT_TO_NEXT_EPOCH, EPOCH_PASSED_PERCET = get_height()
        metric_list['CURRENT_HEIGHT'] = CURRENT_HEIGHT
        metric_list['HEIGHT_TO_NEXT_EPOCH'] = HEIGHT_TO_NEXT_EPOCH
        metric_list['EPOCH_PASSED_PERCET'] = EPOCH_PASSED_PERCET

        # seat price
        VALIDATOR_CURRENT_PRICE, VALIDATOR_NEXT_PRICE, VALIDATOR_PROPOSAL_PRICE = get_seat_price()
        metric_list['VALIDATOR_CURRENT_PRICE'] = VALIDATOR_CURRENT_PRICE
        metric_list['VALIDATOR_NEXT_PRICE'] = VALIDATOR_NEXT_PRICE
        metric_list['VALIDATOR_PROPOSAL_PRICE'] = VALIDATOR_PROPOSAL_PRICE

        # stake amount
        STAKE_AMOUNT, ACCOUNT_TOTAL_BALANCE, ACCOUNT_STAKED_BALANCE, MODIFY_STAKE_AMOUNT, MODIFY_UNSTAKE_AMOUNT = get_stake_amount()
        metric_list['STAKE_AMOUNT'] = STAKE_AMOUNT
        metric_list['ACCOUNT_TOTAL_BALANCE'] = ACCOUNT_TOTAL_BALANCE
        metric_list['ACCOUNT_STAKED_BALANCE'] = ACCOUNT_STAKED_BALANCE

        message_error = "{} Hey <@Sack_UserID>, Near will not be a validator in next epoch.".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        message_ok = "{} Hey <@Sack_UserID>, Near will be a validator in next epoch.".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        RECODE, OUTPUT = get_next_epoch_validator_status()
        VALIDATOR_STATUS = 0
        if OUTPUT == 'Kicked' or RECODE != 0 or OUTPUT == '':
            VALIDATOR_STATUS = -1
            if ALERT_STATUS is False:
                send_to_slack('danger', message_error)
                ping_contract()
                ping_contract(MONITOR_API_URL)
                ALERT_STATUS = True
        elif OUTPUT == 'New':
            VALIDATOR_STATUS = 1
            if ALERT_STATUS is True:
                send_to_slack('good', message_ok)
                ALERT_STATUS = False
        elif OUTPUT == 'Rewarded':
            VALIDATOR_STATUS = 0

        metric_list['VALIDATOR_STATUS'] = VALIDATOR_STATUS
        # send to graphite
        log.info("metric_list: {}".format(metric_list))
        for k, v in metric_list.items():
            path = "{}.{}.{}.{}".format('near', NET, k, hostname)
            send_to_graphite(target_server, path, v, 'pos')
        metric_list.clear()
        time.sleep(60)
