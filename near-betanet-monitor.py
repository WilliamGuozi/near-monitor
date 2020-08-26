import logging
import os
import time
import commands

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
CURRENT_NET_EPOCH_BLOCKS = BetaNet_EPOCH_BLOCKS
RATE = 100000000000000000000
NET = 'betanet'
ACCOUNTID = 'sparkpool.test'
CONTRACTID = 'sparkpool.test'

while True:
    # height
    CURRENT_HEIGHT = """curl -s https://rpc.{}.near.org/status | jq .sync_info.latest_block_height""".format(NET)
    CURRENT_HEIGHT = int(os.popen(CURRENT_HEIGHT).read().strip('\n'))
    EPOCH_START_HEIGHT = """curl -s -d '{"jsonrpc": "2.0", "method": "validators", "id": "dontcare", "params": [null]}' -H 'Content-Type: application/json'""" + """ https://rpc.{}.near.org | jq .result.epoch_start_height""".format(NET)
    EPOCH_START_HEIGHT = int(os.popen(EPOCH_START_HEIGHT).read().strip('\n'))
    HEIGHT_TO_NEXT_EPOCH = EPOCH_START_HEIGHT + CURRENT_NET_EPOCH_BLOCKS - CURRENT_HEIGHT
    EPOCH_PASSED_PERCET = float(CURRENT_HEIGHT - EPOCH_START_HEIGHT) / float(CURRENT_NET_EPOCH_BLOCKS) * 100
    log.info("near current height is {}.".format(CURRENT_HEIGHT))
    log.info("It has {} heights to next epoch.".format(HEIGHT_TO_NEXT_EPOCH))
    log.info("epoch have passed {}%.".format(EPOCH_PASSED_PERCET))
    # seat price
    VALIDATOR_CURRENT_PRICE = """near validators current | awk '/price/ {print substr($6, 1, length($6)-2)}' | sed 's/,//g'"""
    VALIDATOR_CURRENT_PRICE = int(os.popen(VALIDATOR_CURRENT_PRICE).read().strip('\n'))
    log.info("validator current epoch seat price is {}.".format(VALIDATOR_CURRENT_PRICE))

    VALIDATOR_NEXT_PRICE = """near validators next | awk '/price/ {print substr($7, 1, length($7)-2)}' | sed 's/,//g'"""
    VALIDATOR_NEXT_PRICE = int(os.popen(VALIDATOR_NEXT_PRICE).read().strip('\n'))
    log.info("validator next epoch seat price is {}.".format(VALIDATOR_NEXT_PRICE))

    VALIDATOR_PROPOSAL_PRICE = """near proposals | awk '/price =/ {print substr($15, 1, length($15)-1)}' | sed 's/,//g'"""
    VALIDATOR_PROPOSAL_PRICE = int(os.popen(VALIDATOR_PROPOSAL_PRICE).read().strip('\n'))
    log.info("validator proposal price is {}.".format(VALIDATOR_PROPOSAL_PRICE))
    # stake amount
    STAKE_AMOUNT = """near view {} get_account_staked_balance '{{"account_id": "{}"}}' | tail -n1""".format(CONTRACTID, ACCOUNTID)
    STAKE_AMOUNT = int(os.popen(STAKE_AMOUNT).read().strip('\n').split("\'")[1])
    log.info("{} stake amount is {}.".format(ACCOUNTID, STAKE_AMOUNT))
    MODIFY_STAKE_AMOUNT = (VALIDATOR_NEXT_PRICE * RATE) + (100 * RATE) - STAKE_AMOUNT
    log.info("MODIFY_STAKE_AMOUNT: {}".format(MODIFY_STAKE_AMOUNT))
    MODIFY_UNSTAKE_AMOUNT = STAKE_AMOUNT - (VALIDATOR_NEXT_PRICE * RATE) - (100 * RATE)
    log.info("MODIFY_UNSTAKE_AMOUNT: {}".format(MODIFY_UNSTAKE_AMOUNT))
    PING = """near call {} ping '{{}}' --accountId {}""".format(CONTRACTID, ACCOUNTID)

    if MODIFY_UNSTAKE_AMOUNT > 0:
        UNSTAK = """near call {} unstake '{{"amount": "{}"}}' --accountId {}""".format(CONTRACTID, MODIFY_UNSTAKE_AMOUNT, ACCOUNTID)
        RECODE, OUTPUT = commands.getstatusoutput(UNSTAK)
        log.info("{} will unstake {}".format(ACCOUNTID, MODIFY_UNSTAKE_AMOUNT))
        log.info("RECODE: {}, OUTPUT: {}.".format(RECODE, OUTPUT))

    elif MODIFY_STAKE_AMOUNT > 0:
        STAKE = """near call {} stake '{{"amount": "{}"}}' --accountId {}""".format(CONTRACTID, MODIFY_STAKE_AMOUNT, ACCOUNTID)
        RECODE, OUTPUT = commands.getstatusoutput(STAKE)
        log.info("{} will stake {}".format(ACCOUNTID, MODIFY_STAKE_AMOUNT))
        log.info("RECODE: {}, OUTPUT: {}.".format(RECODE, OUTPUT))

    RECODE, OUTPUT = commands.getstatusoutput(PING)
    log.info("RECODE: {}, OUTPUT: {}.".format(RECODE, OUTPUT))
    time.sleep(300)
