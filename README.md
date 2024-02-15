# easydb_urls
webservice to query an easydb instance for urls of the assets
based on tutorial script from Programmfabrik

## Documentation


### Create python virtual environment

    python3 -m venv easydb_urls
    cd easydb_urls

### Activate environment

    source ./bin/activate


### Install easydb_urls scripts in virtual environment
Download scripts and change into scripts directory:

    git clone https://github.com/ZFMK/easydb_urls.git
    cd easydb_urls/
    pip install -r requirements.txt
    python setup.py develop

Copy file `easydb_urls/config.txt` to `easydb_urls/config.ini` and set your needed values there.

Copy file `production.ini.template` to `production.ini` (and for development `development.ini.template` to `development.ini`) and ajust the parameters to your needs.



### Configure Apache webserver

Setup a proxy for the wsgi-server in ssl configuration:

    <virtualhost *:443>
    [...]
    
        # proxy for easydb_urls
        ProxyPass /eaurls http://localhost:6545/eaurls connectiontimeout=5 timeout=300
        ProxyPassReverse /eaurls http://localhost:6545/eaurls
        ProxyPreserveHost On
        ProxyRequests Off
    [...]
    
    </virtualhost>


    
    




