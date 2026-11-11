"""Failure-oriented coverage for the v2 saved-record and private-logit boundaries."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
import reproduce_v2 as v2


class V2Tests(unittest.TestCase):
    def test_public_records(self):
        self.assertEqual(v2.saved_checks(v2.ROOT)['accounting_rows'],246)

    def test_corruption_rejected(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name);(root/'results/v2').mkdir(parents=True)
            (root/'a').write_bytes(b'altered')
            entry={'bytes':7,'sha256':hashlib.sha256(b'correct').hexdigest()}
            (root/'results/v2/manifest.json').write_text(json.dumps({'included':{'a':entry}}))
            with self.assertRaisesRegex(ValueError,'hash mismatch'):
                v2.integrity(root)
            (root/'a').unlink()
            with self.assertRaisesRegex(ValueError,'missing v2 file'):
                v2.integrity(root)

    def test_impossible_accounting_rejected(self):
        with self.assertRaisesRegex(ValueError,'accounting'):
            v2.check_accounting(dict(n=100,correct=90,baseline_correct=90,corrections=2,breaks=0,accuracy=.9))

    def test_wrong_accuracy_rejected(self):
        with self.assertRaisesRegex(ValueError,'accuracy'):
            v2.check_accounting(dict(n=100,correct=90,baseline_correct=90,corrections=0,breaks=0,accuracy=.91))

    def test_private_input_rejected_before_numpy_load(self):
        with tempfile.TemporaryDirectory() as name:
            p=Path(name)/'untrusted.npz';p.write_bytes(b'not authenticated')
            with self.assertRaisesRegex(ValueError,'logits hash mismatch'):
                v2.numerical_checks(v2.ROOT,p)

    def test_missing_external_material_stays_unverified(self):
        omissions=v2.integrity(v2.ROOT)['omitted']
        self.assertIn('reviewer_vectors_and_source',omissions)
        self.assertIn('original_retrospective_verification',omissions)

    def test_groups_partition(self):
        labels=list(range(10))
        self.assertEqual(sum(v2.group_mask(labels,'true8')),1)
        self.assertEqual(sum(v2.group_mask(labels,'non8')),9)
        with self.assertRaisesRegex(ValueError,'unknown group'):
            v2.group_mask(labels,'unsupported')


try:
    import numpy as np
except ImportError:
    np=None


@unittest.skipIf(np is None,'optional NumPy unavailable')
class NumericalBoundaryTests(unittest.TestCase):
    def test_lowest_index_ties_and_direct_subtraction(self):
        z=np.zeros((2,10));z[:,8]=2;z[1,9]=1;z[1,:8]=-1
        self.assertEqual(v2.shifted(np,z,2).tolist(),[0,9])
        self.assertEqual(v2.shifted(np,z,1).tolist(),[8,8])

    def test_candidate_bounds_and_unrestricted_endpoint(self):
        z=np.zeros((2,10));z[:,8]=[2,5]
        self.assertEqual(v2.candidates(np,z,True),[0,1,2,2.5,3])
        self.assertEqual(v2.candidates(np,z,False),[0,1,2,3.5,5,10])


if __name__=='__main__':
    unittest.main()
