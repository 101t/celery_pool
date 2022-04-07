# Celery Queue Implementation

to try it on local, install the required package:

```sh
virtualenv -p python3 env
source env/bin/activate

pip install -r requirements.txt
```

In Terminal, Run Entrypoint shell-script command to run Celery:
```sh
./entrypoint.sh
```

Open another terminal, and activate environment then log into python interactive shell then run the following code:
```python
from tasks import test

test()
```
