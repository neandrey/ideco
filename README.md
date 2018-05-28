
####intro
Установка и настройка пакета:

Загрузка через йогурт

    yaourt -S squid

Для создания /var/cach/squid
    
    squid -k check
    squid -z

Запуск

    systemctl start squid.service
    systemctl enable squid.service

Основные команды

    # squid -k reconfigure # restart the server each time you tweak your redirector
    # squid -k interrupt # bring squid to a stop
    # squid -k check # is it running?

####Настройка
Открываем порт 3128.

    firewall-cmd --add-port=3128/tcp
    firewall-cmd --add-port=3128/tcp --permanent

Настройка firefox для работы через proxy.

    Perferenct -> network proxy -> manual прописываем хост:порт


Для перенаправления необходимо написать вспомогательную программу (программа помошник). Которая получает запрос из `stdin` обрабатывает его и отправляет в `stdout`. Форматы ввода и вывода представлены в [Документации.](http://wiki.squid-cache.org/Features/Redirectors) 

*   Для начало я написал программу которая получает данные из входной строки и записывает их в файл который располагается /var/cache/squid/
*   Разобравшись с форматом и как обрабатывать входные данные я написал основную программу.
*   Вопрос возник с перенаправлением Яндекса отправляет на какой-то  portal-xiva.yandex.net:443 решил пока оставить разобраться потом. 

Да для работы программы необходимо:

*   `url_rewrite_extras "%>a %>rm %un"` # формат ввода с `stdin`
*   `url_rewrite_children 3 startup=0 idle=1 concurrency=10` # вспомогательные процессы.
*   `url_rewrite_program /etc/squid/squid-redirect.py` #место расположения вспомогательной программы








