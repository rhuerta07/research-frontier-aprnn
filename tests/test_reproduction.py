"""Targeted evidence mutation tests; no model or solver dependencies."""
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('reproduce_tables', ROOT/'analysis/reproduce_tables.py')
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)


class ReproductionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        shutil.copytree(ROOT/'results', self.root/'results')
        for folder in ('paper', 'protocols', 'reviews'):
            shutil.copytree(ROOT/folder, self.root/folder)

    def change(self, path, function):
        p = self.root/path
        obj = json.loads(p.read_text())
        function(obj)
        p.write_text(json.dumps(obj))

    def fails(self, message=None):
        with self.assertRaisesRegex(ValueError, message or '.'):
            r.analyze(self.root, integrity=False)

    def test_known_results(self):
        out = r.analyze(self.root)
        self.assertEqual(out['rp001']['P001_J0']['domains']['fog_primary'], dict(baseline_correct=1771, correct=5087, corrections=3538, breaks=222))
        self.assertEqual(out['rp001']['P002_J1']['domains']['identity_primary']['correct'], 8348)
        self.assertAlmostEqual(out['rp001']['P002_fog_primary_J1_minus_J0_pp'], 100*288/8900)
        self.assertAlmostEqual(out['pilot']['fog']['ratio'], .5750869341986871)
        self.assertAlmostEqual(out['pilot']['clean']['ratio'], 1.461189253524856)
        self.assertEqual(out['pilot']['joint_decision'], 'NO-GO')

    def test_small_transition_example(self):
        d=dict(indices=[0,1,2,3], labels=[0,1,2,3], baseline=[0,0,2,0], predictions=[1,1,2,0])
        self.assertEqual(r.counts(d,0,4), dict(baseline_correct=2,correct=2,corrections=1,breaks=1))

    def test_changed_label_alignment(self):
        self.change('results/evidence/P001_J0/common_setup.json', lambda x:x['labels'].__setitem__(0, 9))
        self.fails('selected labels')

    def test_missing_label(self):
        with self.assertRaisesRegex(ValueError, 'denominator'):
            r.counts(dict(indices=[0],labels=[],baseline=[0],predictions=[0]),0,1)

    def test_index_alignment(self):
        with self.assertRaisesRegex(ValueError, 'index alignment'):
            r.counts(dict(indices=[1],labels=[0],baseline=[0],predictions=[0]),0,1)

    def test_inconsistent_denominator(self):
        self.change('results/rp001_summary.json', lambda x:x['pairs']['P001']['domains']['fog_primary'].__setitem__('n',9000))
        self.fails('denominator')

    def test_altered_cohort_identity(self):
        self.change('results/pilot_summary.json', lambda x:x['records'][0].__setitem__('id','P999'))
        self.fails('cohort identities')

    def test_missing_attempt(self):
        self.change('results/rp001_summary.json', lambda x:x['slots'].pop('P002_J1'))
        self.fails('repair attempts')

    def test_malformed_json(self):
        p=self.root/'results/rp001_summary.json';p.write_text('{bad')
        self.fails()

    def test_duplicate_keys(self):
        p=self.root/'results/rp001_summary.json';p.write_text('{"x":1,"x":2}')
        self.fails('duplicate JSON key')

    def test_nonfinite_json(self):
        p=self.root/'results/rp001_summary.json';p.write_text('{"x":NaN}')
        self.fails('nonfinite')

    def test_incorrect_correction_break_accounting(self):
        self.change('results/rp001_summary.json', lambda x:x['pairs']['P001']['domains']['fog_primary']['j0'].__setitem__('breaks',221))
        self.fails('correction/break')

    def test_source_tampering(self):
        p=self.root/'results/evidence/P001_J0/independent_heldout_predictions.json'
        p.write_bytes(p.read_bytes()+b' ')
        with self.assertRaisesRegex(ValueError, 'size mismatch'):
            r.analyze(self.root)

    def test_missing_file(self):
        (self.root/'results/evidence/P001_J0/independent_heldout_predictions.json').unlink()
        with self.assertRaisesRegex(ValueError, 'missing evidence'):
            r.analyze(self.root)

    def test_missing_outcome_cannot_be_imputed(self):
        self.change('results/pilot_summary.json', lambda x:x['records'][4].__setitem__('outcomes',{}))
        self.fails('missingness')

    def test_changed_joint_screen(self):
        self.change('results/pilot_summary.json', lambda x:x.__setitem__('numerical_screen',True))
        self.fails('NO-GO')


if __name__ == '__main__':
    unittest.main()
