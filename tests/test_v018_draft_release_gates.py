from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import subprocess
import tempfile
import unittest
import yaml

from tools.v018_draft_release_gates import GATE_IDS, validate_record, validate_transition, validate_candidate_binding, PHASE_GATE_STATES


ROOT = Path(__file__).resolve().parents[1]


class V018ReleaseGateContractTests(unittest.TestCase):
    def test_transition_baseline_record_is_bounded_and_explicit(self):
        from tools.v018_draft_release_gates import load_readiness_document, RECORD_RELATIVE
        record, _ = load_readiness_document(ROOT / RECORD_RELATIVE)
        result = subprocess.run(
            ['git', 'show', f"{record['base_sha']}:{RECORD_RELATIVE}"],
            cwd=ROOT, check=True, capture_output=True, text=True,
        )
        baseline_text = result.stdout
        end = baseline_text.index('\n---\n', 4)
        baseline = yaml.safe_load(baseline_text[4:end])
        self.assertEqual('evidence_candidate', baseline['phase'])
        self.assertEqual('v0.18-draft', baseline['release'])
        self.assertEqual('v0.18-draft', baseline['milestone'])
        self.assertEqual('not_applicable', baseline['gates']['standards_mapping']['state'])
        self.assertNotIn('qualified_crosswalk_review', GATE_IDS)
        self.assertTrue(all(item['state'] == ('not_applicable' if gate == 'standards_mapping' else 'open') for gate, item in baseline['gates'].items()))
        self.assertEqual([], validate_record(ROOT, baseline))

    def test_rejects_premature_version_advancement_and_missing_ordinary_gate(self):
        from tools.v018_draft_release_gates import load_readiness_document, RECORD_RELATIVE
        record, _ = load_readiness_document(ROOT / RECORD_RELATIVE)
        record = deepcopy(record)
        record['version_advanced'] = True
        record['gates']['technical']['state'] = 'closed'
        errors = validate_record(ROOT, record)
        self.assertTrue(any('version_advanced shall remain false' in e for e in errors))
        self.assertTrue(any('technical' in e for e in errors))

    def test_phase_state_contracts(self):
        from tools.v018_draft_release_gates import PHASE_GATE_STATES
        self.assertEqual('open', PHASE_GATE_STATES['evidence_candidate']['technical'])
        self.assertEqual('not_applicable', PHASE_GATE_STATES['evidence_candidate']['standards_mapping'])
        self.assertEqual('ready', PHASE_GATE_STATES['closure_candidate']['technical'])
        self.assertEqual('closed', PHASE_GATE_STATES['published']['technical'])
        self.assertEqual('not_applicable', PHASE_GATE_STATES['published']['standards_mapping'])

    def test_closure_candidate_requires_ordinary_gate_evidence(self):
        from tools.v018_draft_release_gates import load_readiness_document, RECORD_RELATIVE, PHASE_GATE_STATES
        record, _ = load_readiness_document(ROOT / RECORD_RELATIVE)
        record = deepcopy(record)
        record['phase'] = 'closure_candidate'
        record['gates'] = {
            gate: {'state': state, 'evidence': [] if gate in {'post_merge', 'standards_mapping'} else ['https://github.com/tdistress/ESAF/issues/224']}
            for gate, state in PHASE_GATE_STATES['closure_candidate'].items()
        }
        record['gates']['technical']['evidence'] = []
        errors = validate_record(ROOT, record)
        self.assertTrue(any('technical evidence is required' in error for error in errors))

    def test_malformed_gates_and_standards_mapping_fail_without_exception(self):
        from tools.v018_draft_release_gates import load_readiness_document, RECORD_RELATIVE
        record, _ = load_readiness_document(ROOT / RECORD_RELATIVE)
        for malformed in (None, [], 'not-a-gate-map'):
            candidate = deepcopy(record)
            candidate['gates'] = malformed
            self.assertTrue(validate_record(ROOT, candidate))
        candidate = deepcopy(record)
        candidate['gates']['standards_mapping'] = 'not-a-gate-object'
        self.assertTrue(any('standards_mapping' in error for error in validate_record(ROOT, candidate)))

    def test_published_publication_evidence_must_be_a_list(self):
        from tools.v018_draft_release_gates import load_readiness_document, RECORD_RELATIVE, PHASE_GATE_STATES
        record, _ = load_readiness_document(ROOT / RECORD_RELATIVE)
        record = deepcopy(record)
        record['phase'] = 'published'
        record['gates'] = {
            gate: {'state': state, 'evidence': [] if gate == 'standards_mapping' else ['https://github.com/tdistress/ESAF/actions/runs/1']}
            for gate, state in PHASE_GATE_STATES['published'].items()
        }
        record['publication'] = {
            'condition': 'annotated_tag_targets_validated_closure_candidate',
            'tag_object': 'a' * 40,
            'tagged_commit': 'b' * 40,
            'date': '2026-10-07',
            'evidence': 17,
        }
        errors = validate_record(ROOT, record)
        self.assertTrue(any('published publication evidence shall be a list' in error for error in errors))

    def test_candidate_binding_requires_committed_readiness_but_allows_unrelated_dirty_files(self):
        from tools.v018_draft_release_gates import RECORD_RELATIVE
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            subprocess.run(['git', 'init', '-q'], cwd=repo, check=True)
            subprocess.run(['git', 'config', 'user.email', 'release-test@example.invalid'], cwd=repo, check=True)
            subprocess.run(['git', 'config', 'user.name', 'Release Test'], cwd=repo, check=True)
            record_path = repo / RECORD_RELATIVE
            record_path.parent.mkdir(parents=True)
            committed_text = '---\nphase: evidence_candidate\n---\n'
            record_path.write_text(committed_text, encoding='utf-8')
            subprocess.run(['git', 'add', str(record_path.relative_to(repo))], cwd=repo, check=True)
            subprocess.run(['git', 'commit', '-qm', 'candidate'], cwd=repo, check=True)
            self.assertEqual([], validate_candidate_binding(repo, committed_text))
            (repo / 'unrelated.tmp').write_text('unrelated dirty artifact', encoding='utf-8')
            self.assertEqual([], validate_candidate_binding(repo, committed_text))
            record_path.write_text(committed_text + 'uncommitted edit\n', encoding='utf-8')
            self.assertTrue(any('differs from committed HEAD' in error for error in validate_candidate_binding(repo, record_path.read_text(encoding='utf-8'))))

    def test_published_record_can_follow_annotated_tag_target(self):
        from tools.v018_draft_release_gates import load_readiness_document, RECORD_RELATIVE
        record, _ = load_readiness_document(ROOT / RECORD_RELATIVE)
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            subprocess.run(['git', 'init', '-q'], cwd=repo, check=True)
            subprocess.run(['git', 'config', 'user.email', 'release-test@example.invalid'], cwd=repo, check=True)
            subprocess.run(['git', 'config', 'user.name', 'Release Test'], cwd=repo, check=True)
            path = repo / RECORD_RELATIVE
            path.parent.mkdir(parents=True)
            closure = deepcopy(record)
            closure['phase'] = 'closure_candidate'
            closure['base_sha'] = '0' * 40
            closure['gates'] = {
                gate: {'state': state, 'evidence': [] if gate in {'post_merge', 'standards_mapping'} else ['https://github.com/tdistress/ESAF/pull/224']}
                for gate, state in PHASE_GATE_STATES['closure_candidate'].items()
            }
            closure['publication'] = {'condition': 'annotated_tag_targets_validated_closure_candidate', 'tag_object': None, 'tagged_commit': None, 'date': None, 'evidence': []}
            def save(value):
                path.write_text('---\n' + yaml.safe_dump(value, sort_keys=False) + '---\n\n# v0.18-draft publication readiness\n\n## Scope\n\n## Mandatory gates\n\n## Lifecycle boundary\n\n## Publication evidence\n', encoding='utf-8')
                subprocess.run(['git', 'add', str(path.relative_to(repo))], cwd=repo, check=True)
                subprocess.run(['git', 'commit', '-qm', 'record readiness'], cwd=repo, check=True)
            save(closure)
            closure_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip()
            subprocess.run(['git', 'tag', '-a', 'v0.18-draft', '-m', 'v0.18-draft'], cwd=repo, check=True)
            tag_object = subprocess.check_output(['git', 'rev-parse', 'refs/tags/v0.18-draft'], cwd=repo, text=True).strip()
            published = deepcopy(closure)
            published['phase'] = 'published'
            published['base_sha'] = closure_sha
            published['gates'] = {gate: {'state': state, 'evidence': [] if gate == 'standards_mapping' else ['https://github.com/tdistress/ESAF/actions/runs/1']} for gate, state in PHASE_GATE_STATES['published'].items()}
            published['publication'] = {'condition': 'annotated_tag_targets_validated_closure_candidate', 'tag_object': tag_object, 'tagged_commit': closure_sha, 'date': '2026-10-07', 'evidence': ['https://github.com/tdistress/ESAF/issues/224']}
            save(published)
            self.assertNotEqual(closure_sha, subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip())
            self.assertEqual([], validate_transition(repo, closure_sha, published))
            wrong_target = deepcopy(published)
            wrong_target['publication']['tagged_commit'] = 'f' * 40
            self.assertTrue(any('equal the exact closure_candidate baseline SHA' in error for error in validate_transition(repo, closure_sha, wrong_target)))
            stale = deepcopy(published)
            stale['publication']['tag_object'] = 'f' * 40
            self.assertTrue(any('tag object is stale' in error for error in validate_transition(repo, closure_sha, stale)))
            stale_base = deepcopy(published)
            stale_base['base_sha'] = 'f' * 40
            self.assertTrue(any('base_sha shall equal the exact baseline' in error for error in validate_transition(repo, closure_sha, stale_base)))
            published_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=repo, text=True).strip()
            (repo / 'unrelated.txt').write_text('maintenance', encoding='utf-8')
            subprocess.run(['git', 'add', 'unrelated.txt'], cwd=repo, check=True)
            subprocess.run(['git', 'commit', '-qm', 'published maintenance'], cwd=repo, check=True)
            maintenance = deepcopy(published)
            maintenance['base_sha'] = published_sha
            self.assertEqual([], validate_transition(repo, published_sha, maintenance))
            mutated = deepcopy(maintenance)
            mutated['publication']['date'] = '2026-10-08'
            self.assertTrue(any('identity and closed gate truth' in error for error in validate_transition(repo, published_sha, mutated)))
            mutated_gate = deepcopy(maintenance)
            mutated_gate['gates']['technical']['evidence'] = ['https://github.com/tdistress/ESAF/issues/changed']
            self.assertTrue(any('identity and closed gate truth' in error for error in validate_transition(repo, published_sha, mutated_gate)))
            regressed = deepcopy(maintenance)
            regressed['phase'] = 'closure_candidate'
            regressed['gates'] = closure['gates']
            self.assertTrue(any('transition only from evidence_candidate' in error for error in validate_transition(repo, published_sha, regressed)))
