# near-monitor
For near monitor

# install dep env
```bash
pip install colorlog graphyte
```



# Testnet Monitor

## Run command
> near-testnet-monitor.py 中一个参数要根据你的实际情况赋值 目标 graphite 服务器地址 `target_server`
```
nohup /root/near-daemon.sh testnet >> near-daemon.log 2>&1 &
```

## log
```
2020-08-26 15:31:38,248 INFO     near current height is 13363781.0.
2020-08-26 15:31:38,248 INFO     It has 27194.0 heights to next epoch.
2020-08-26 15:31:38,248 INFO     epoch have passed 37.0509259259%.
2020-08-26 15:31:40,108 INFO     validator current epoch seat price is 48518.
2020-08-26 15:31:40,108 INFO     validator next epoch seat price is 47478.
2020-08-26 15:31:40,108 INFO     validator proposal price is 46804.
2020-08-26 15:31:41,980 INFO     sparkpool.testnet stake amount is 1.07988423788e+29.
2020-08-26 15:31:42,615 INFO     get_next_epoch_validator_status RECODE: 0, OUTPUT: Rewarded.
2020-08-26 15:31:42,615 INFO     metric_list: {'EPOCH_PASSED_PERCET': 37.050925925925924, 'ACCOUNT_STAKED_BALANCE': 3434.2673858272283, 'VALIDATOR_CURRENT_PRICE': 48518, 'HEIGHT_TO_NEXT_EPOCH': 27194.0, 'VALIDATOR_PROPOSAL_PRICE': 46804, 'VALIDATOR_STATUS': 0, 'CURRENT_HEIGHT': 13363781.0, 'ACCOUNT_TOTAL_BALANCE': 3434.2673858272283, 'VALIDATOR_NEXT_PRICE': 47478, 'STAKE_AMOUNT': 107988.4237877982}
2020-08-26 15:31:42,615 INFO     sending graphite data path: near.testnet.EPOCH_PASSED_PERCET.pos-test-hk-01, metric: 37.0509259259
2020-08-26 15:31:42,706 INFO     sending graphite data path: near.testnet.ACCOUNT_STAKED_BALANCE.pos-test-hk-01, metric: 3434.26738583
2020-08-26 15:31:42,773 INFO     sending graphite data path: near.testnet.VALIDATOR_CURRENT_PRICE.pos-test-hk-01, metric: 48518
2020-08-26 15:31:42,845 INFO     sending graphite data path: near.testnet.HEIGHT_TO_NEXT_EPOCH.pos-test-hk-01, metric: 27194.0
2020-08-26 15:31:42,926 INFO     sending graphite data path: near.testnet.VALIDATOR_PROPOSAL_PRICE.pos-test-hk-01, metric: 46804
2020-08-26 15:31:43,008 INFO     sending graphite data path: near.testnet.VALIDATOR_STATUS.pos-test-hk-01, metric: 0
2020-08-26 15:31:43,084 INFO     sending graphite data path: near.testnet.CURRENT_HEIGHT.pos-test-hk-01, metric: 13363781.0
2020-08-26 15:31:43,152 INFO     sending graphite data path: near.testnet.ACCOUNT_TOTAL_BALANCE.pos-test-hk-01, metric: 3434.26738583
2020-08-26 15:31:43,236 INFO     sending graphite data path: near.testnet.VALIDATOR_NEXT_PRICE.pos-test-hk-01, metric: 47478
2020-08-26 15:31:43,320 INFO     sending graphite data path: near.testnet.STAKE_AMOUNT.pos-test-hk-01, metric: 107988.423788
```
## 效果展示
>数据发送至graphite后可以参考 我的博客文章<https://www.cnblogs.com/William-Guozi/p/grafana-monitor.html> 组建和呈现监控

![img-w500](/images/202008260418.png)



# Betanet Challenge
## Run command
```
nohup /root/near-daemon.sh betanet>> near-daemon.log 2>&1 &
```


## log

```
2020-07-08 16:26:43,803 INFO     near current height is 9054836.
2020-07-08 16:26:43,803 INFO     It has 6044 heights to next epoch.
2020-07-08 16:26:43,803 INFO     epoch have passed 39.56%.
2020-07-08 16:26:45,945 INFO     validator current epoch seat price is 112328.
2020-07-08 16:26:48,159 INFO     validator next epoch seat price is 112878.
2020-07-08 16:26:50,334 INFO     validator proposal price is 112409.
2020-07-08 16:26:51,663 INFO     sparkpool.test stake amount is 11297799999999999999999999.
2020-07-08 16:26:51,663 INFO     MODIFY_STAKE_AMOUNT: 1
2020-07-08 16:26:51,663 INFO     MODIFY_UNSTAKE_AMOUNT: 19999999999999999999999
2020-07-08 16:27:01,161 INFO     sparkpool.test will unstake 19999999999999999999999
2020-07-08 16:27:01,161 INFO     RECODE: 0, OUTPUT: Using options: { accountId: 'sparkpool.test',
  networkId: 'betanet',
  nodeUrl: 'https://rpc.betanet.near.org',
  contractName: 'sparkpool.test',
  walletUrl: 'https://wallet.betanet.near.org',
  helperUrl: 'https://helper.betanet.near.org',
  helperAccount: 'betanet',
  useLedgerKey: '44\'/397\'/0\'/0\'/1\'',
  gas: '100000000000000',
  amount: '0',
  methodName: 'unstake',
  args: '{"amount": "19999999999999999999999"}',
  initialBalance: null }
Scheduling a call: sparkpool.test.unstake({"amount": "19999999999999999999999"})
[sparkpool.test]: @sparkpool.test unstaking 20000000000000000000000. Spent 11501103911883886566473 staking shares. Total 9518490942606742532160268226 unstaked balance and 6485357484872204795968744 staking shares
[sparkpool.test]: Contract total staked balance is 202143270560578513684674403563. Total number of shares 116243537990263621375644494599
''.
2020-07-08 16:27:07,081 INFO     RECODE: 0, OUTPUT: Using options: { accountId: 'sparkpool.test',
  networkId: 'betanet',
  nodeUrl: 'https://rpc.betanet.near.org',
  contractName: 'sparkpool.test',
  walletUrl: 'https://wallet.betanet.near.org',
  helperUrl: 'https://helper.betanet.near.org',
  helperAccount: 'betanet',
  useLedgerKey: '44\'/397\'/0\'/0\'/1\'',
  gas: '100000000000000',
  amount: '0',
  methodName: 'ping',
  args: '{}',
  initialBalance: null }
Scheduling a call: sparkpool.test.ping({})
''.
```
