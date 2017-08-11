
#查密钥生成工具路径
find / -name keytool

/usr/java/jdk1.7.0_15/bin/keytool -genkey -alias tomcat -keyalg RSA -keystore /usr/local/tomcat/tomcat.keystore -validity 36500
密码：111111
主机：访问IP或域名


#配置SSL接口
vim server.xml
8080 ---> 443
443 ---> keystoreFile="/usr/local/tomcat/apache-tomcat-7.0.37/tomcat.keystore" keystorePass="111111"

#针对war的自动拦截跳转
vim web.xml
<login-config>
<!-- Authorization setting for SSL -->
<auth-method>CLIENT-CERT</auth-method>
    <realm-name>Client Cert Users-only Area</realm-name>
    </login-config>
    <security-constraint>
        <!-- Authorization setting for SSL -->
<web-resource-collection >
        <web-resource-name >[转SSL的war包名称]</web-resource-name>
                <url-pattern>/*</url-pattern>
                    </web-resource-collection>
                        <user-data-constraint>
                                <transport-guarantee>CONFIDENTIAL</transport-guarantee>
                                    </user-data-constraint>
                                    </security-constraint>
