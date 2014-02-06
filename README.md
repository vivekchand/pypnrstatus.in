pypnrstatus.in
==============

Web App of py-pnr-status ( https://github.com/vivekchand/py-pnr-status )

![alt tag](https://raw.github.com/vivekchand/pypnrstatus.in/master/pypnrstatus.png)

Dev Setup in Local:
-------------------
```python
step1: python manage.py syncdb  # Creates Database

step2: sh bin/web  # Starts Web Server & Worker
              or
       python manage.py runserver
       python worker.py
```

ToDo:
-----
1. Stop sending notifications when ticket is cancelled / journey happened / chart prepared / ticket confirmed.
