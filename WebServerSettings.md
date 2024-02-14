
#### How to change Server Headers Presented to Clients

In the file /etc/apache2/conf-enabled/security.conf file, you navigate to the ServerTokens field and change the value - choose **Prod** for the least information about the server given in the response headers, choose **Full** for the most information given. Restart the apache2 server as required. 

```
# The setting configured below to withhold the most info about the server
# in the response headers. 
ServerTokens Prod
```

#### How to Enable and Disable HTTP Trace Requests

Disable TRACE HTTP requests by turning off the TraceEnable field in the security.conf file. Restart the apache2 server as required.

```
# The setting configured below to disable TRACE requests to the server. 
TraceEnable Off
```

*Velasco: "Okay so these requests are used for debugging. They return the error trace in the http response's headers."*


#### How to Enable and Disable Directory Browsing

Need to find the following portion of the apache2.conf file:

```
    <Directory>
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
```

and change it to 

```
    <Directory>
        Options FollowSymLinks
        AllowOverride None
        Require all granted
    </Directory>
```

Removing the `Indexes` portion in the Options disables directory listing generation in the apache2 webserver. Thus, raw directory browsing will no longer be possible. 
