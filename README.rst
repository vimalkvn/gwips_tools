Scripts for updating annotations and reference sequences from UCSC
==================================================================
The following scripts from gwips_tools can be used to update genome annotations
and RefSeq's from UCSC.

* update_annotations.py
* update_refseq.py


Requirements
------------
**MySQL server and MySQL-python package**

On Ubuntu 14.04, you can install the following packages to get
all the requirements - ``mysql-server``, ``libmysqlclient-dev`` and
``python-mysqldb``.


Usage
-----
For both the scripts, the ``-h`` flag prints a help message.

To get the list of all available genomes from configuration::

    sudo python update_annotations.py -l

To update annotations for a genome for example, hg19::

    sudo python update_annotations.py -g hg19

Reload MySQL::

    sudo service mysql reload

To update RefSeq's::

    sudo python update_refseq.py -g hg19

For convenience, a sample bash script is included which can be used to update the
annotations followed by the reference sequences. Copy ``update_all.sh.sample`` to
``update_all.sh`` and then modify the list of genomes to update and the path.

`Why sudo? <sudo>`_

Configuration - adding/updating available genomes
-------------------------------------------------
List of available genomes is done in the file ``config.json``. Additional
genomes can be added to the "genomes" section. Datasets to download can be
specified in the "datasets" key of the respective genome.

Other variables

``source_url``:
    Source URL for downloading the mysql tables.

``target_dir``:
    Downloaded MySQL tables are stored in this directory.

``refseq_source_url``:
    Source URL for RefSeq sequences.

``refseq_target_dir``:
    Downloaded RefSeq's are stored in this directory.

``refseq_user``:
    User with write privileges to ``refseq_target_dir``.

``annotations_user``:
    User with write privileges to ``target_dir``.

.. _sudo:

Note regarding permissions
--------------------------
User/group id's for downloaded files are set in ``config.json`` ::

    annotations_user = 'mysql'  # for mysql tables
    refseq_user = 'vimal'  # for refseq sequences

Both the update scripts are run using ``sudo`` for the following reason.

update_annotations.py requires write access to ``/var/lib/mysql`` which is owned
by ``mysql``. When downloading datasets, the user and group id is changed to that
of the ``mysql`` user (``annotations_user``) on the system.

update_refseq.py downloads sequences to directory specified under 
``refseq_target_dir``. These are owned by user specified in ``refseq_user``.

Tests
-----
Please copy ``tests/data/config.json.sample`` to ``tests/data/config.json``
Change paths for ``refseq_target_dir``, ``target_dir`` and ``backup_dir``.

Now run the test suite from the main source directory ::

    sh runtests.sh

Test configuration can be updated in ``gwips_tools/config.py``.
