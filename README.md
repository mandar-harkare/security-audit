## Prerequisite

*   Python
*   pip



## Steps

*   Run through following commands
```
pip install -r requirements.txt
```

or

```
pip3 install -r requirements.txt
```

*   Login to aws cli

*   Assume role for the account
```
aws sts assume-role --role-arn arn:aws:iam::[account_id]:role/[role_name] --role-session-name session_name
```

```
python sg.py
```

or

```
python3 sg.py
```

Your results will be saved in the test.xlsx