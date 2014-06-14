from fabric.api import *
from fabric.contrib.files import exists
from fabtools import require
import fabtools
import time

MYSQL_PASSWORD = ""
WORDPRESS_USER_NAME = ""
FFT_WORDPRESS_USER_PASSWORD = ""
DB_PRODUCTION_HOST = ""
PRODUCTION_KEYNAME = ""
BLOG_NAME = ""

env.roledefs = {
    'development': ['vagrant@127.0.0.1:2222'],
    'production': [''],
}

env.root_dir = '/home/%s' % WORDPRESS_USER_NAME
env.wp_config = "conf/wordpress/wp-config-sample"

if (env.roles[0]=="development"):
    result = local('vagrant ssh-config | grep IdentityFile', capture=True)
    env.key_filename = result.split()[1].strip('"')
    env.wp_config = "%s-development.php" % env.wp_config

#settings based on role production
if (env.roles[0]=="production"):
    env.key_filename = '~/keys/' % PRODUCTION_KEYNAME
    env.wp_config = "%s-production.php" % env.wp_config

def provision():
    #update APT package definitions
    fabtools.deb.update_index(quiet=False)

    #Require a sudo user
    fabtools.require.users.user(WORDPRESS_USER_NAME)
    fabtools.require.users.sudoer(WORDPRESS_USER_NAME, hosts='ALL', operators='ALL', passwd=False, commands='ALL')

    # Require a mysql server
    require.mysql.server(password=WORDPRESS_USER_PASSWORD)
    
    # Require a nginx server running
    require.nginx.server()
    
    # Require some Debian/Ubuntu packages
    require.deb.packages([
        'php5-fpm',
        'php5-mysql',
    ])
    
    #transfer project
    transfer_project()
    
    #install wordpress
    install_wordpress()

    # Restart servers
    restart_servers()

def install_wordpress():
    #download and install wordpress if not previously done
    with cd(env.root_dir):
        if not exists("wordpress"):
            sudo("wget http://wordpress.org/latest.tar.gz")
            sudo("tar -xzvf latest.tar.gz")
            sudo("rm -f latest.tar.gz")
        if (env.roles[0]=="development"):
            sudo("mysql --user=root --password=%s < conf/init.sql" % WORDPRESS_USER_PASSWORD)
        #transfer wp-config.php
        sudo("cp -rf %s wordpress/wp-config.php" % env.wp_config)
        #transfer wordpress/languages to wordpress/wp-content/language
        sudo("cp -rf conf/wordpress/languages/ wordpress/wp-content/")
        #transfer wordpress/plugins to wordpress/wp-content/plugins
        sudo("cp -rf conf/wordpress/plugins/ wordpress/wp-content/")
        #transfer wordpress/themes to wordpress/wp-content/themes
        sudo("cp -rf conf/wordpress/themes/ wordpress/wp-content/")
        #create www-dir
        if not exists("/var/www/%s" % BLOG_NAME):
            sudo("mkdir -p /var/www/%s" % BLOG_NAME)
        #transfer wordpress
        sudo("cp -r wordpress/* /var/www/")
        sudo("cp -r wordpress/* /var/www/%s" % BLOG_NAME)
        with cd("/var/www/"):
            sudo("chown www-data:www-data * -R")
            sudo("usermod -a -G www-data %s" % WORDPRESS_USER_NAME)
    print "installed wordpress"

def restart_servers():
    with cd(env.root_dir):
        sudo("cp -f conf/nginx.conf /etc/nginx/sites-available/default")
        sudo("cp -f conf/php.ini /etc/php5/fpm/php.ini")
    sudo("service php5-fpm restart")
    sudo("/etc/init.d/nginx restart")

def transfer_project():
    #make file structure for release
    release_name = time.strftime("%Y%m%d%H%M%S")
    with cd(env.root_dir):
        #makes an archive from git using git-archive-all https://github.com/Kentzo/git-archive-all
        local("git-archive-all release_%s.tar.gz" % (release_name))
        put("release_%s.tar.gz" % (release_name), env.root_dir, use_sudo=True)
        sudo("tar zxf release_%s.tar.gz" % (release_name))
        sudo("rm -f release_%s.tar.gz" % (release_name))
        local("rm -f release_%s.tar.gz" % (release_name))
        sudo("cp -rf www /usr/share/nginx/")

def deploy():
    transfer_project()
    install_wordpress()
    restart_servers()

def backup_conf():
    get('/etc/php5/fpm/php.ini','conf/php.ini.backup')

def backup_wordpress():
    backup_name = "wordpress_backup_%s.sql" % time.strftime("%Y%m%d%H%M%S")
    with cd(env.root_dir):
        if (env.roles[0]=="development"):
            sudo("mysqldump --add-drop-table --user=root --password=%s wordpress > backups/%s" % (WORDPRESS_USER_PASSWORD, backup_name))
        if (env.roles[0]=="production"):
            sudo("mysqldump --add-drop-table -h %s -P 3306 -u master -p wordpress > backups/%s" % (DB_PRODUCTION_HOST, backup_name))
        get("backups/%s"%(backup_name),"backups/%s" % (backup_name))
        local("git add -A")

def restore_backup(name):
    with cd(env.root_dir):
        if (env.roles[0]=="development"):
            sudo("mysql --user=root --password=%s wordpress < backups/%s" % (WORDPRESS_USER_PASSWORD,name))
        if (env.roles[0]=="production"):
            sudo("mysql -h %s -P 3306 -u master -p wordpress < backups/%s" % (DB_PRODUCTION_HOST, name))