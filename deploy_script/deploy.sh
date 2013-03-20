#!/bin/bash
###################################################################
#                         deploy script                           #
# 　　一个简单的部署脚本，在创建Apache虚拟主机配置同时，添加SVN仓 #
# 库并做一个钩子自动更新到Apache Web根目录                        #
#                                                     2013-03-09  #
#                                                         shenhd  #
###################################################################

##### define variables #####
PROJECT=$1

SVN_ROOT=PATH/svn
SVNADMIN_BIN=/usr/bin/svnadmin
SVN_BIN=/usr/bin/svn
SVN_USER=USER
SVN_PWD=PASSWORD

WEB_ETC=APACHE_CONF_DIR
WEB_ROOT=APACHE_HTDOC_DIR
WEB_USER=www
WEB_GROUP=www

HOST_PREFIX=
HOST_SUFFIX=
##### define variables #####

if [ "${UID}" != "0" ]
then
	echo Please grant it root privileges
	exit
elif [ "${PROJECT}" == "" ]
then
	echo Please specify a project name
	exit
fi

function create_svn() {
	SVN_REPO=${SVN_ROOT}/${PROJECT}
	
	# create project svn repository
	$SVNADMIN_BIN create ${SVN_REPO}
	
	# backup config files
	mv ${SVN_REPO}/conf/svnserve.conf ${SVN_REPO}/conf/svnserve.conf.orgin
	mv ${SVN_REPO}/conf/authz ${SVN_REPO}/conf/authz.orgin
	mv ${SVN_REPO}/conf/passwd ${SVN_REPO}/conf/passwd.orgin

	cp ./conf/svnserve.conf ${SVN_REPO}/conf/
	cp ./conf/authz ${SVN_REPO}/conf/
	sed -i "s/PROJECT/${PROJECT}/g" ${SVN_REPO}/conf/authz
	cp ./conf/passwd ${SVN_REPO}/conf/

	if [ ! -f "${SVN_REPO}/conf/authz" ] || [ ! -f "${SVN_REPO}/conf/passwd" ] \
		|| [ ! -f "${SVN_REPO}/conf/svnserve.conf" ]
	then
		echo Cannot change configure files for svn
		exit
	fi
}

function create_host() {
	PROJECT_ETC=${WEB_ETC}/${PROJECT}.conf
	PROJECT_ROOT=${WEB_ROOT}/${PROJECT}
	
	mkdir -p ${PROJECT_ROOT}

	if [ ! -d ${PROJECT_ROOT} ]
	then
		echo Cannot create project htdoc root
		exit
	fi
	
	# change directory owner
	chown -R ${WEB_USER}:${WEB_GROUP} ${PROJECT_ROOT}

	cp ./conf/host.conf ${PROJECT_ETC}
	
	sed -i "s/PROJECT_HOST/${HOST_PREFIX}${PROJECT}${HOST_SUFFIX}/g" ${PROJECT_ETC}
	sed -i "s/PROJECT/${PROJECT}/g" ${PROJECT_ETC}
}

function hook_svn() {
	${SVN_BIN} checkout svn://127.0.0.1/${PROJECT} --username ${SVN_USER} --password ${SVN_PWD} ${PROJECT_ROOT}

	cp ./conf/post-commit ${SVN_REPO}/hooks/
	chmod +x ${SVN_REPO}/hooks/post-commit
	HOOK=${SVN_REPO}/hooks/post-commit
	sed -i "s/WEB_USER/${WEB_USER}/g" ${HOOK}
	sed -i "s/SVN_USER/${SVN_USER}/g" ${HOOK}
	sed -i "s/SVN_PWD/${SVN_PWD}/g" ${HOOK}
	WEBROOT=${PROJECT_ROOT//\//\\\/}
	sed -i "s/PROJECT_ROOT/${WEBROOT}/g" ${HOOK}
}

create_svn
create_host
hook_svn

echo Reload your web server.
