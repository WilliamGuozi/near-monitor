# near-monitor
For near monitor


# Run command
```
python near-monitor2.py >> near-monitor.log 2>&1 &
```

# log

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
