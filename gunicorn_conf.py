bind = '127.0.0.1:8081'

workers = 5
# если воркер не отвечает, через это время его выключить
timeout = 30
#pidfile = '/run/askme/askme.pid'
#errorlog = '/var/log/gunicorn/askme.log'
#chdir = '/home/keith/PycharmProjectsPro/AskMe'
# для просмотра в таблице процессов
proc_name = 'askme_gunicorn'

#ExecStart = /home/vagrant/askme/venv/bin/gunicorn askme:app -b 127.0.0.1:8000
# --pid /run/askme/askme.pid
# --log-file /var/log/gunicorn/askme.log
# --chdir /home/vagrant/askme