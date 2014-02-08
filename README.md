pypnrstatus.in
==============

Web App of py-pnr-status ( https://github.com/vivekchand/py-pnr-status )

![alt tag](https://raw.github.com/vivekchand/pypnrstatus.in/master/pypnrstatus.png)

Dev Setup in Local:
-------------------
```
step0: pip install -r requirements.txt

step1: python manage.py syncdb  # Creates Database

step2: sh bin/web  # Starts Web Server & Worker
              or
       python manage.py runserver
       python worker.py
       
step3: Go to http://127.0.0.1:8000/       
```

ToDo:
-----
1. Better form validation
