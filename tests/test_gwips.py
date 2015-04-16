import os
import unittest
import tempfile
from gwips_tools import gwips_tools, config

CONFIG = config.TestingConfig()
print 'Using configuration file: ', CONFIG.CONFIG_FILE


class GwipsTestCase(unittest.TestCase):

    def setUp(self):
        gwips_tools.check_config_json(CONFIG.CONFIG_FILE)
        self.vals = gwips_tools.read_config(CONFIG.CONFIG_FILE)

    def tearDown(self):
        os.remove(CONFIG.CONFIG_FILE)
        for dirname in (self.vals['genomes'][CONFIG.GENOME]['target_dir'],
                        self.vals['refseq_target_dir']):
            for root, dirs, files in os.walk(dirname, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))


# @unittest.skip('done')
class RsyncTestCase(GwipsTestCase):

    def test_run_rsync(self):
        """A test run of rsync. """
        src = os.path.join(CONFIG.DATA_DIR, u'local/file1.txt')
        dst = tempfile.mkstemp()[1]
        gwips_tools.run_rsync(src, dst)
        self.assertTrue(os.path.exists(dst))
        os.remove(dst)

    def test_sync_file(self):
        """Test syncing a real dataset. """
        vals = gwips_tools.read_config(CONFIG.CONFIG_FILE)
        genome = vals['genomes'][CONFIG.GENOME]  # hg19
        gwips_tools.download_mysql_table(
            os.path.join(genome['source_url']),
            os.path.join(genome['target_dir']), genome['datasets'][0]
        )
        for ext in ('.MYD', '.MYI', '.frm'):
            self.assertTrue(
                os.path.exists(
                    os.path.join(genome['target_dir'],
                                 '{0}{1}'.format(genome['datasets'][0], ext))))


class RefSeqTestCase(GwipsTestCase):

    def test_download_refseq(self):
        """Given the list of mRNA fasta files from database, download both
        mRNA and Protein FASTA sequences to refseq_target_dir

        """
        refseq_paths = [open(
            os.path.join(CONFIG.DATA_DIR, 'missing.fa')).readline().strip()]

        # use one refseq file for test purposes
        mrnas, peps = gwips_tools.download_refseqs(
            refseq_paths, self.vals['refseq_source_url'],
            self.vals['refseq_target_dir'])
        self.assertTrue(os.path.exists(mrnas[0]), "mRNA Fasta must be present")
        self.assertTrue(os.path.exists(peps[0]), "Peptide fasta must be present")


# @unittest.skip('done')
class ConfigTestCase(GwipsTestCase):

    def test_read_config(self):
        """rsync URL and datasets must be read from config for an entry. """
        vals = gwips_tools.read_config(CONFIG.CONFIG_FILE)
        genome = vals['genomes'][CONFIG.GENOME]
        self.assertEqual(genome['source_url'],
                         'rsync://hgdownload.cse.ucsc.edu/mysql/hg19/')
        self.assertTrue(len(genome['datasets']) > 1)

    def test_create_config(self):
        """Test if config.json can be created from sample. """
        config_file = os.path.join(CONFIG.DATA_DIR, 'config.json')
        gwips_tools.check_config_json(config_file)
        self.assertTrue(os.path.exists(config_file))

if __name__ == '__main__':
    unittest.main()
