FROM registry.ischool.syr.edu:5000/ndlyga/django-pillow:1.0

COPY uwsgi.ini /etc/uwsgi/uwsgi.ini

COPY requirements.txt /var/webapp/requirements.txt

RUN pip install -r /var/webapp/requirements.txt

COPY ./ischool_profiles /var/webapp

WORKDIR /var/webapp

COPY entrypoint.sh /usr/local/bin/entrypoint.sh

RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 9000

# Command to run the sites
CMD ["/bin/bash", "/usr/local/bin/entrypoint.sh"]