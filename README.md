# Splits Calculator

Very basic script that can turn timestamps into formatted splits as well as
compare formatted splits.

## Turning timestamps into splits
Run the script then input the timestamps of when all the things happen. It'll
assume the first timestamp is for the run starting and use it as an offset for
all the others. Also put the actual finish time at the end on its own line.
(Once finished input Control+Z for python to know you're done.)

For example:
```
python splits_calculator.py
0:50 Run start
2:11 Charger zone
5:30 Shadow zone
8:11 Run complete
7:21
```
will turn into:
```
` 1:21 (1:21)` Charger zone
` 4:40 (3:19)` Shadow zone
` 7:21 (2:41)` Run complete
```
which renders beautifully in markdown (or discord, which uses markdown syntax)
as:\
` 1:21 (1:21)` Charger zone\
` 4:40 (3:19)` Shadow zone\
` 7:21 (2:41)` Run complete

## Comparing splits
You can also paste in two sets of formatted splits in order to compare them.
It'll give both your time-gain/loss per split as well as the cumulative
time-gain/loss over the run so far.

For example:
```
python splits_calculator.py -c
1:21 (1:21) Charger zone
4:40 (3:19) Shadow zone
7:21 (2:41) Run complete

1:42 (1:42) Charger zone
4:50 (3:08) Shadow zone
7:10 (2:20) Run complete
```
will turn into:
```
`+21  1:42 (+21 1:42)` Charger zone
`+10  4:50 (-11 3:08)` Shadow zone
`-11  7:10 (-21 2:20)` Run complete
```
which when rendered gives:\
`+21  1:42 (+21 1:42)` Charger zone\
`+10  4:50 (-11 3:08)` Shadow zone\
`-11  7:10 (-21 2:20)` Run complete
