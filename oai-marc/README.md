
DESCRIPTION

Harverst OAI-PMH 2.0 record set and validate data.

INSTALL
<pre>
apt-get install python-setuptools python-lxml python-six yaz-client

<a href="https://pypi.org/project/pyoai/#files">pyoai-2.5.0.tar.gz</a>

tar xzf pyoai-2.5.0.tar.gz
cd pyoai-2.5.0
python -B setup.py install

<a href="https://pypi.org/project/pymarc/#files">pymarc-3.1.13.tar.gz</a>

tar xzf pymarc-3.1.13.tar.gz
cd pymarc-3.1.13
python -B setup.py install

/usr/local/bin/:

oai-7
oai-kat
oai-5xx
oai-marc
oai-daily
oai-weekly
oai-monthly
oai-monthly-7
oai-monthly-kat

country_code.txt
lang_code.txt
role_code.txt
sif_code.txt

/etc/crontab:

00 5 * * * root oai-daily >> /var/log/oai-daily.log 2>&1 &
00 6 * * TUE root oai-weekly >> /var/log/oai-weekly.log 2>&1 &
30 6 2 * * root oai-monthly >> /var/log/oai-monthly.log 2>&1 &
00 4 1 * * root oai-monthly-7 >> /var/log/oai-monthly-7.log 2>&1 &
00 5 1 * * root oai-monthly-kat >> /var/log/oai-monthly-kat.log 2>&1 &
</pre>
APACHE
<pre>
        DocumentRoot /var/www/html

        &lt;Directory /var/www/html&gt;
                Options +Indexes
                HeaderName /include/HEADER.html
                ReadmeName /include/README.html
                AddIcon /icons/world2.gif ..
                IndexOptions FancyIndexing FoldersFirst NameWidth=* DescriptionWidth=* HTMLTable IgnoreClient
                IndexOptions SuppressHTMLPreamble SuppressDescription SuppressLastModified SuppressSize SuppressRules SuppressColumnSorting
                IndexIgnore .??* include *.csv
                IndexStyleSheet /include/STYLE.css
                AllowOverride Indexes
        &lt;/Directory&gt;

        &lt;Directory /var/www/html/nkp/&gt;
                Options +Indexes
                HeaderName /nkp/include/HEADER.html
                ReadmeName /nkp/include/README.html
                AddIcon /icons/world2.gif ..
                IndexOptions FancyIndexing FoldersFirst NameWidth=* DescriptionWidth=* HTMLTable IgnoreClient
                IndexOptions SuppressHTMLPreamble SuppressDescription SuppressLastModified SuppressSize SuppressRules SuppressColumnSorting
                IndexIgnore .. .??* include
                IndexStyleSheet  /nkp/include/STYLE.css
                AllowOverride Indexes 
        &lt;/Directory&gt;

        &lt;Directory /var/www/html/nkp/*/&gt;
                Options +Indexes
                HeaderName /nkp/include/HEADER.html
                ReadmeName /nkp/include/README.html
                AddIcon /icons/world2.gif ..
                IndexOptions FancyIndexing FoldersFirst NameWidth=* DescriptionWidth=* HTMLTable IgnoreClient
                IndexOptions SuppressHTMLPreamble SuppressDescription SuppressLastModified SuppressSize SuppressRules SuppressColumnSorting
                IndexIgnore .??* include
                IndexStyleSheet  /nkp/include/STYLE.css
                AllowOverride Indexes 
        &lt;/Directory&gt;
</pre>
FILE
<pre>
           html/ - Apache AutoIndexing HTML structure.
            773/ - Covert Aleph record 773 to 856.

        oai-marc - OAI-OMH 2.0 MARCXML record validation.
         oai-5xx - Send dumped 245/246/5xx text for correction. 
         oai-mdt - Z39.50 yaz-client wrapper.
           oai-7 - Evaluate subfield "7" data. 
         oai-kat - Evaluate field "KAT" data. 
       oai-7-xml - Evaluate subfield "7" datafrom file.
        oai-file - Debug & testing.

       oai-daily - Crontab daily runner.
      oai-weekly - Crontab weekly runner.
     oai-monthly - Crontab monthly runner.
   oai-monthly-7 - Crontab "7" monthly runner.
 oai-monthly-kat - Crontab "KAT" monthly runner.

  field.py.patch - Allow non-standard control field(FMT).

country_code.txt - MARC country code file.
   lang_code.txt - MARC language code file.
   role_code.txt - MARC role code file.
    sif_code.txt - MARC sif code file.
</pre>
SOURCE

https://github.com/KyomaHooin/UCL

