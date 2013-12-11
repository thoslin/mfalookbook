from fabric.api import env, sudo, local, put
from fabric.context_managers import prefix


def vagrant():
    env.user = 'vagrant'
    env.hosts = ['127.0.0.1:2222']

    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1].strip('"')


def install_packages():
    packages = [
        "python-pip",
        "python-virtualenv",
        "git-core",
        "supervisor",
        "g++",
        "curl",
        "python-dev",
        "libxml2-dev",
        "libxslt-dev",
        "nginx",
    ]
    sudo("apt-get -y update")
    sudo("apt-get -y install %s" % " ".join(packages))


def create_user():
    sudo("useradd mfa -m -g www-data -s /bin/bash")
    sudo("mkdir -p /home/mfa/{src,logs}", user="mfa")


def copy_ssh_keys():
    put("~/.ssh", "/home/mfa/", use_sudo=True)
    sudo("chown -R mfa /home/mfa/.ssh")
    sudo("chmod 644 /home/mfa/.ssh/config /home/mfa/.ssh/id_rsa.pub")
    sudo("chmod 600 /home/mfa/.ssh/id_rsa")


def setup_repo():
    sudo("git clone git@bitbucket.org:thoslin/mfalookbook.git /home/mfa/src/", user="mfa")


def setup_virtualenv():
    sudo("virtualenv /home/mfa/venv", user="mfa")
    with prefix("source /home/mfa/venv/bin/activate"):
        sudo("pip install -r /home/mfa/src/mfa/requirements.txt", user="mfa")


def setup_supervisor():
    sudo("ln -s /home/mfa/src/mfa/mfa/lookbook/config/supervisor.gunicorn.conf /etc/supervisor/conf.d/")
    sudo("supervisorctl reload")


def setup_nginx():
    sudo("cp /home/mfa/src/mfa/mfa/lookbook/config/nginx.mfa.conf /etc/nginx/sites-available/")
    sudo("ln -s /etc/nginx/sites-available/nginx.mfa.conf /etc/nginx/sites-enabled/nginx.mfa.conf")
    sudo("service nginx restart")


def setup_cron():
    sudo('crontab < /home/mfa/src/mfa/mfa/lookbook/config/mfa_cronjob', user="mfa")

def remove_ssh_keys():
    sudo("rm /home/mfa/.ssh -rf")


def deploy():
    install_packages()
    create_user()
    copy_ssh_keys()
    setup_repo()
    setup_virtualenv()
    setup_supervisor()
    setup_nginx()
    setup_cron()
    remove_ssh_keys()


def restart_app():
    sudo("supervisorctl reload mfa-gunicorn")