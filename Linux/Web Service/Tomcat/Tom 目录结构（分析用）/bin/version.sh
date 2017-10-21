#!/bin/sh

# -----------------------------------------------------------------------------
# 查看Tomcat的版本、操作系统信息
#Using CATALINA_BASE:   /usr/local/tomcat8
#Using CATALINA_HOME:   /usr/local/tomcat8
#Using CATALINA_TMPDIR: /usr/local/tomcat8/temp
#Using JRE_HOME:        /usr/jdk18
#Using CLASSPATH:       /usr/local/tomcat8/bin/bootstrap.jar:/usr/local/tomcat8/bin/tomcat-juli.jar
#Server version: Apache Tomcat/8.0.38
#Server built:   Oct 6 2016 20:51:55 UTC
#Server number:  8.0.38.0
#OS Name:        Linux
#OS Version:     2.6.32-431.el6.i686
#Architecture:   i386
#JVM Version:    1.8.0_101-b13
#JVM Vendor:     Oracle Corporation
# -----------------------------------------------------------------------------

# Better OS/400 detection: see Bugzilla 31132
os400=false
case "`uname`" in
OS400*) os400=true;;
esac

# resolve links - $0 may be a softlink
PRG="$0"

while [ -h "$PRG" ] ; do
  ls=`ls -ld "$PRG"`
  link=`expr "$ls" : '.*-> \(.*\)$'`
  if expr "$link" : '/.*' > /dev/null; then
    PRG="$link"
  else
    PRG=`dirname "$PRG"`/"$link"
  fi
done

PRGDIR=`dirname "$PRG"`
EXECUTABLE=catalina.sh

# Check that target executable exists
if $os400; then
  # -x will Only work on the os400 if the files are:
  # 1. owned by the user
  # 2. owned by the PRIMARY group of the user
  # this will not work if the user belongs in secondary groups
  eval
else
  if [ ! -x "$PRGDIR"/"$EXECUTABLE" ]; then
    echo "Cannot find $PRGDIR/$EXECUTABLE"
    echo "The file is absent or does not have execute permission"
    echo "This file is needed to run this program"
    exit 1
  fi
fi

exec "$PRGDIR"/"$EXECUTABLE" version "$@"
