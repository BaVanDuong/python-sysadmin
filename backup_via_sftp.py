import tarfile
import paramiko
from datetime import datetime
import socket
import os
import platform


if __name__ == '__main__':

    linux_dist = platform.linux_distribution()[0]
    if linux_dist == 'Ubuntu':
        httpd_conf = '/etc/apache2'

    elif linux_dist == 'CentOS':
        httpd_conf = 'etc/httpd'
    www = '/var/www'

    backup_dir = '/tmp/backup'

    if not os.path.exists(backup_dir):
        os.mkdir(backup_dir)

    date_now = datetime.now()
    hostname = socket.gethostname()

    # create apache backup file
    httpd_file = hostname + '.httpd.' + \
        date_now.strftime('%Y-%m-%d') + '.tar.gz'

    httpd_backup_path = os.path.join(backup_dir, httpd_file)

    with tarfile.open(httpd_backup_path, 'w:gz') as tar:
        tar.add(httpd_conf, arcname=os.path.basename(httpd_conf))
        tar.add(www, arcname=os.path.basename(www))

    # create ssh session
    SERVER = '192.168.1.18'
    PORT = 22
    USER = 'backup'
    PASSWD = 'helloworld'

    try:
        try:
            remote_path = '/backup'
            transport = paramiko.Transport((SERVER, PORT))
            transport.connect(username=USER, password=PASSWD)
            sftp = paramiko.SFTPClient.from_transport(transport)
            # upload
            sftp.put(httpd_backup_path, os.path.join(remote_path, httpd_file))
        # close connection
        finally:
            sftp.close()
            transport.close()
    except:
        print 'Connect to {}:{} failed!'.format(SERVER, PORT)
    else:
        print 'Upload file {0} to {1}:{2} successfully.'.format(httpd_file,
                                                                SERVER, PORT)
