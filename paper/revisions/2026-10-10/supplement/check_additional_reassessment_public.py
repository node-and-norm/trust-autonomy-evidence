"""Offline additional-reassessment checker, public packaging derivative of version 2.

Reproduces supplied classifications; does not validate their evidentiary basis.
The original ZIP is a byte-pinned, read-only dependency included in this bundle.
"""
import argparse
import base64
import io
import copy
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys
import zipfile

CONDITIONS = ['access', 'comprehension', 'authority', 'feasibility', 'exercise', 'propagation']
STATES = ('S', 'P', 'U', 'I')
RESULTS = ('Pass', 'Fail', 'Unresolved')
ORIGINAL_SHA256 = '9ddfa8651d14e5a9f041ce906215e7fc8e3152bdd22d848a7270ea9d6e90ac76'
RULE = {'priority': ['any_U', 'all_S', 'otherwise_P_or_I'], 'any_U': 'Fail', 'all_S': 'Pass',
        'otherwise_P_or_I': 'Unresolved', 'change_from_released_rule': 'none'}


class InputError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise InputError(message)


def fields(value, names, where):
    require(type(value) is dict, where + ': object required')
    require(set(value) == set(names.split()), where + ': missing or unexpected field')


def nonempty(value, where):
    require(type(value) is str and bool(value.strip()), where + ': nonempty string required')


def digest(content):
    return hashlib.sha256(content).hexdigest()


def duplicate_check(pairs):
    out = {}
    for key, value in pairs:
        require(key not in out, 'duplicate JSON key: ' + key)
        out[key] = value
    return out


def json_read(content):
    return json.loads(content, object_pairs_hook=duplicate_check)


def safe_filename(name):
    require(type(name) is str and Path(name).name == name and name not in ('', '.', '..'), 'local file basename required')
    return name


def check_reference(ref):
    safe_filename(ref['file'])
    require(type(ref['sha256']) is str and re.fullmatch('[0-9a-f]{64}', ref['sha256']) is not None, 'invalid SHA-256')


def options(cell):
    values = [cell] if type(cell) is str else cell
    require(type(values) is list and len(values) > 0, 'nonempty state or alternatives required')
    require(all(type(s) is str and s in STATES for s in values), 'invalid state')
    require(len(set(values)) == len(values), 'duplicate state alternative')
    return values


def aggregate(row):
    require(type(row) in (list, tuple) and len(row) == 6, 'exactly six required states')
    require(all(type(s) is str and s in STATES for s in row), 'invalid/missing state')
    if 'U' in row:
        return 'Fail'
    if row.count('S') == 6:
        return 'Pass'
    return 'Unresolved'


def validate(data, previous):
    fields(data, 'schema_version supplement_id status condition_order aggregation_rule case_names previous_supplement additional_source public_approval additional_reassessment counterfactuals limits', 'input')
    require(type(data['schema_version']) is int and data['schema_version'] == 3, 'schema version must be 3')
    require(data['supplement_id'] == 'additional-reassessment-v2-public-2026-10-10', 'unexpected supplement version')
    require(data['status'] == 'public_release_candidate_pending_packaging_check', 'public packaging status changed')
    require(data['condition_order'] == CONDITIONS, 'fixed condition order changed')
    require(data['aggregation_rule'] == RULE, 'unchanged aggregation rule changed')
    names = {c['case_id']: c['name'] for c in previous['cases']}
    require(data['case_names'] == names, 'case identity/names differ from preserved dependency')
    prior = data['previous_supplement']
    fields(prior, 'file sha256 original_filename recorded_inputs_member recorded_inputs_sha256 results_member ledger_member ledger_sha256 relationship', 'previous_supplement')
    check_reference(prior)
    require(prior['sha256'] == ORIGINAL_SHA256, 'original supplement identity changed')
    for key, value in prior.items():
        nonempty(value, 'previous_supplement.' + key)
    fields(data['additional_source'], 'file sha256 status', 'additional_source')
    check_reference(data['additional_source'])
    nonempty(data['additional_source']['status'], 'source status')
    fields(data['public_approval'], 'file sha256 approval_date author', 'public_approval')
    check_reference(data['public_approval'])
    for key in ('approval_date', 'author'):
        nonempty(data['public_approval'][key], 'public_approval.' + key)
    item = data['additional_reassessment']
    fields(item, 'assessment_id base_stage adoption_status result_status stage_3_amendments_adopted rows changes_from_stage_2 dependencies', 'additional_reassessment')
    require(item['assessment_id'] == 'additional_zg710_reassessment_v2' and item['base_stage'] == 'stage_2', 'assessment identity/base changed')
    require(item['adoption_status'] == 'author_approved_revised_preprint_and_additional_reassessment', 'approval scope changed')
    require(item['result_status'] == 'conditional_on_accepted_assessor_judgments_and_retained_Stage_2_inputs', 'conditional dependencies changed')
    require(item['stage_3_amendments_adopted'] is False, 'Stage 3 amendments are unapproved')
    original_rows = previous['stages'][1]['rows']
    frozen = [{'case_id': r['case_id'], 'states': copy.deepcopy(r['states'])} for r in original_rows]
    require(type(item['rows']) is list and len(item['rows']) == 3, 'three case rows required')
    for row in item['rows']:
        fields(row, 'case_id states', 'row')
        require(type(row['states']) is list and len(row['states']) == 6, 'six condition cells required')
        for cell in row['states']:
            options(cell)
    changes = item['changes_from_stage_2']
    require(type(changes) is list and len(changes) == 3, 'exactly three approved additional changes required')
    expected_changes = [('comprehension', 'I'), ('feasibility', ['P', 'I']), ('exercise', ['P', 'I'])]
    for change, (condition, replacement) in zip(changes, expected_changes):
        fields(change, 'case_id condition from to basis', 'change')
        require(change['case_id'] == 'TAE-PUB-002' and change['condition'] == condition, 'change outside approved ZG710 cells')
        require(change['from'] == 'U' and change['to'] == replacement, 'approved state disposition changed')
        nonempty(change['basis'], 'change basis')
        row = next(r for r in frozen if r['case_id'] == change['case_id'])
        idx = CONDITIONS.index(condition)
        require(row['states'][idx] == change['from'], 'original Stage 2 cell mismatch')
        row['states'][idx] = copy.deepcopy(change['to'])
    require(item['rows'] == frozen, 'additional rows do not match Stage 2 plus only the approved changes')
    require(type(item['dependencies']) is list and bool(item['dependencies']), 'dependencies required')
    for entry in item['dependencies']:
        nonempty(entry, 'dependency')
    cf = data['counterfactuals']
    fields(cf, 'base case_id conditions replacement status', 'counterfactuals')
    require(cf['base'] == item['assessment_id'] and cf['case_id'] == 'TAE-PUB-002', 'counterfactual base/case changed')
    require(cf['conditions'] == ['comprehension', 'feasibility', 'exercise'] and cf['replacement'] == 'U', 'counterfactual changes invalid')
    require(cf['status'] == 'rule_illustrations_only_not_adopted_states_or_empirical_sensitivity_analysis', 'counterfactual status changed')
    require(type(data['limits']) is list and bool(data['limits']), 'limitations required')
    for entry in data['limits']:
        nonempty(entry, 'limit')


def load_dependencies(data, base):
    require(type(data) is dict and type(data.get('previous_supplement')) is dict, 'previous_supplement object required')
    ref = data['previous_supplement']
    require(type(ref.get('file')) is str, 'previous supplement filename required')
    raw = base64.b64decode((base / safe_filename(ref['file'])).read_bytes().strip(), validate=True)
    require(digest(raw) == ORIGINAL_SHA256, 'original supplement bytes changed')
    with zipfile.ZipFile(io.BytesIO(raw)) as archive:
        previous_bytes = archive.read(ref.get('recorded_inputs_member', ''))
        previous = json_read(previous_bytes)
        saved = json_read(archive.read(ref.get('results_member', '')))
        ledger_bytes = archive.read(ref.get('ledger_member', ''))
    validate(data, previous)
    require(digest(previous_bytes) == ref['recorded_inputs_sha256'], 'original recorded-input identity mismatch')
    require(digest(ledger_bytes) == ref['ledger_sha256'], 'original ledger identity mismatch')
    for key in ('additional_source', 'public_approval'):
        require(digest((base / data[key]['file']).read_bytes()) == data[key]['sha256'], key + ': file hash mismatch')
    approval = json_read((base / data['public_approval']['file']).read_bytes())
    fields(approval, 'schema_version author approval_date statement scientific_scope interpretive_limit release_status', 'public approval statement')
    require(approval['schema_version'] == 1, 'public approval statement schema changed')
    for field in ('statement', 'scientific_scope', 'interpretive_limit', 'release_status'):
        nonempty(approval[field], 'public approval statement.' + field)
    require(approval['approval_date'] == data['public_approval']['approval_date'] == '2026-10-10' and approval['author'] == data['public_approval']['author'] == 'Mark Julius Banasihan', 'public_approval provenance mismatch')
    return previous, saved


def explain(row):
    result = aggregate(row)
    u = [{'condition': c, 'state': s} for c, s in zip(CONDITIONS, row) if s == 'U']
    unknown = [{'condition': c, 'state': s} for c, s in zip(CONDITIONS, row) if s in ('P', 'I')]
    return {'states': list(row), 'result': result,
            'state_counts': {s: row.count(s) for s in STATES},
            'decisive_U_cells': u,
            'unresolved_blocking_cells': unknown if result == 'Unresolved' else [],
            'nondecisive_P_I_cells_when_Fail': unknown if result == 'Fail' else []}


def evaluate(rows, names, group_id, status):
    cases = []
    for row in rows:
        variants = [{'variant_id': i, **explain(list(values))}
                    for i, values in enumerate(itertools.product(*(options(c) for c in row['states'])), 1)]
        result_set = [r for r in RESULTS if any(v['result'] == r for v in variants)]
        cases.append({'case_id': row['case_id'], 'name': names[row['case_id']], 'recorded_states': row['states'],
                      'alternative_count': len(variants), 'possible_results': result_set,
                      'result_invariant': len(result_set) == 1, 'alternatives': variants})
    joint = []
    for number, combination in enumerate(itertools.product(*(c['alternatives'] for c in cases)), 1):
        joint.append({'combination_id': number,
                      'case_variant_ids': {c['case_id']: v['variant_id'] for c, v in zip(cases, combination)},
                      'case_results': {c['case_id']: v['result'] for c, v in zip(cases, combination)},
                      'case_result_counts': {r: sum(v['result'] == r for v in combination) for r in RESULTS},
                      'cell_state_counts': {s: sum(v['state_counts'][s] for v in combination) for s in STATES}})
    totals = sorted(set(tuple(j['case_result_counts'][r] for r in RESULTS) for j in joint))
    vectors = set(tuple(j['case_results'][c['case_id']] for c in cases) for j in joint)
    return {'group_id': group_id, 'status': status, 'cases': cases, 'joint_assignment_count': len(joint),
            'case_result_vector_invariant': len(vectors) == 1, 'case_result_counts_invariant': len(totals) == 1,
            'possible_case_result_counts': [dict(zip(RESULTS, t)) for t in totals],
            'cell_state_count_ranges': {s: {'min': min(j['cell_state_counts'][s] for j in joint), 'max': max(j['cell_state_counts'][s] for j in joint)} for s in STATES},
            'joint_assignments': joint}


def compute(data, previous):
    names = data['case_names']
    historical = [evaluate(s['rows'], names, s['stage_id'], 'unchanged_archived_comparison') for s in previous['stages'][:2]]
    item = data['additional_reassessment']
    added = evaluate(item['rows'], names, item['assessment_id'], item['result_status'])
    counterfactuals = []
    for condition in data['counterfactuals']['conditions']:
        rows = copy.deepcopy(item['rows'])
        row = next(r for r in rows if r['case_id'] == data['counterfactuals']['case_id'])
        row['states'][CONDITIONS.index(condition)] = data['counterfactuals']['replacement']
        result = evaluate(rows, names, 'single_U_at_' + condition, data['counterfactuals']['status'])
        result['explanation'] = 'Restore one justified necessary-condition U; no unknown elsewhere can cancel it. This is a rule illustration, not an adopted state change.'
        counterfactuals.append(result)
    return {'unchanged_historical_comparisons': historical, 'additional_reassessment': added,
            'single_U_counterfactuals': counterfactuals,
            'stage_3': 'Broader amendments remain unapproved. Stage 3 is preserved inside the original ZIP and is not adopted by this supplement.'}


def self_tests(data, previous, saved):
    tests = []
    def check(ok, label):
        if not ok:
            raise RuntimeError('SELF-TEST FAILED: ' + label)
    counts = {r: 0 for r in RESULTS}
    for row in itertools.product(STATES, repeat=6):
        result = aggregate(row)
        check((result == 'Fail') == (row.count('U') > 0), 'any U')
        check((result == 'Pass') == (row.count('S') == 6), 'all S')
        check((result == 'Unresolved') == (row.count('U') == 0 and row.count('S') < 6), 'unknown without U')
        counts[result] += 1
    check(counts == {'Pass': 1, 'Fail': 3367, 'Unresolved': 728}, '4^6 rule distribution')
    tests.append({'name': 'all_4096_legal_rows', 'passed': True, 'counts': counts})
    n = 0
    for index in range(6):
        for other in itertools.product(('S', 'P', 'I'), repeat=5):
            row = list(other); row.insert(index, 'U')
            check(aggregate(row) == 'Fail' and not explain(row)['unresolved_blocking_cells'], 'single-U dominance/explanation')
            n += 1
    tests.append({'name': 'explicit_U_dominance_at_all_six_positions', 'passed': True, 'rows': n})
    check(aggregate(['S'] * 6) == 'Pass', 'explicit all-S')
    for index in range(6):
        for value in ('P', 'I'):
            row = ['S'] * 6; row[index] = value
            check(aggregate(row) == 'Unresolved', 'explicit single unknown')
    tests.append({'name': 'all_S_and_12_single_unknown_cases', 'passed': True})
    invalid = [None, [], 'SSSSSS', ['S'] * 5, ['S'] * 7]
    for state in ('', 'X', None, True, 0, {}, ['P', 'I'], 'P/I', 's'):
        invalid.append(['S', 'S', state, 'S', 'S', 'S'])
    for row in invalid:
        try: aggregate(row)
        except InputError: pass
        else: raise RuntimeError('SELF-TEST FAILED: invalid state accepted')
    tests.append({'name': 'invalid_or_missing_state_rejection', 'passed': True, 'rows': len(invalid)})
    paths = []
    def visit(value, path):
        if type(value) is dict:
            for key, child in value.items():
                paths.append(path + [key]); visit(child, path + [key])
        elif type(value) is list:
            for index, child in enumerate(value): visit(child, path + [index])
    visit(data, [])
    for path in paths:
        changed = copy.deepcopy(data); target = changed
        for key in path[:-1]: target = target[key]
        del target[path[-1]]
        try: validate(changed, previous)
        except (InputError, TypeError): pass
        else: raise RuntimeError('SELF-TEST FAILED: missing field accepted ' + repr(path))
    mutations = []
    def mutate(path, value):
        changed = copy.deepcopy(data); target = changed
        for key in path[:-1]: target = target[key]
        target[path[-1]] = value; mutations.append(changed)
    mutate(['schema_version'], True)
    mutate(['condition_order'], list(reversed(CONDITIONS)))
    mutate(['aggregation_rule', 'priority'], ['all_S', 'otherwise_P_or_I', 'any_U'])
    mutate(['previous_supplement', 'file'], '../outside.zip')
    mutate(['previous_supplement', 'sha256'], '0' * 64)
    mutate(['additional_reassessment', 'stage_3_amendments_adopted'], True)
    mutate(['additional_reassessment', 'rows', 0, 'states'], ['S'] * 6)
    mutate(['additional_reassessment', 'rows', 1, 'states', 1], 'P')
    mutate(['additional_reassessment', 'rows', 1, 'states', 2], 'S')
    mutate(['additional_reassessment', 'rows', 1, 'states', 3], [])
    mutate(['additional_reassessment', 'rows', 1, 'states', 3], ['P', 'P'])
    mutate(['additional_reassessment', 'rows', 2, 'states', 5], 'U')
    mutate(['additional_reassessment', 'changes_from_stage_2', 0, 'to'], 'P')
    mutate(['counterfactuals', 'replacement'], 'P')
    mutate(['unexpected'], 'field')
    for changed in mutations:
        try: validate(changed, previous)
        except (InputError, TypeError): pass
        else: raise RuntimeError('SELF-TEST FAILED: invalid input accepted')
    try: json_read('{"state":"S","state":"U"}')
    except InputError: pass
    else: raise RuntimeError('SELF-TEST FAILED: duplicate key accepted')
    tests.append({'name': 'input_schema_and_scope_rejection', 'passed': True,
                  'missing_fields': len(paths), 'invalid_mutations': len(mutations), 'duplicate_key': 1})
    outputs = compute(data, previous)
    for current, archived in zip(outputs['unchanged_historical_comparisons'], saved['calculations']['main_stages'][:2]):
        check(current['possible_case_result_counts'] == archived['possible_case_result_counts'], 'preserved historical totals')
        check(current['joint_assignment_count'] == archived['joint_assignment_count'], 'preserved enumeration')
        for now_case, old_case in zip(current['cases'], archived['cases']):
            check(now_case['recorded_states'] == old_case['recorded_state_cells'], 'preserved historical states')
            check(now_case['possible_results'] == old_case['possible_results'], 'preserved historical case results')
    tests.append({'name': 'original_Stage_1_and_Stage_2_regression', 'passed': True, 'stages': 2})
    added = outputs['additional_reassessment']
    check([c['alternative_count'] for c in added['cases']] == [1, 16, 4] and added['joint_assignment_count'] == 64, 'full Cartesian enumeration')
    check(added['case_result_vector_invariant'] and added['case_result_counts_invariant'], 'invariance over allowed assignments')
    for cf in outputs['single_U_counterfactuals']:
        zg = next(c for c in cf['cases'] if c['case_id'] == 'TAE-PUB-002')
        check(zg['possible_results'] == ['Fail'], 'justified single U gives Fail')
        check(all(v['state_counts']['U'] == 1 and len(v['decisive_U_cells']) == 1 and not v['unresolved_blocking_cells'] for v in zg['alternatives']), 'single-U case explanations')
    tests.append({'name': 'additional_64_assignments_and_3_retained_U_illustrations', 'passed': True})
    rows = copy.deepcopy(data['additional_reassessment']['rows'])
    rows[0]['states'] = ['S'] * 6
    check(evaluate(rows, data['case_names'], 'probe', 'test')['cases'][0]['possible_results'] == ['Pass'], 'input-driven all-S')
    rows[0]['states'][0] = 'U'
    check(evaluate(rows, data['case_names'], 'probe', 'test')['cases'][0]['possible_results'] == ['Fail'], 'input-driven U')
    tests.append({'name': 'computed_results_depend_on_input_states', 'passed': True, 'in_memory_mutations': 2})
    return {'status': 'PASS', 'groups': tests}


def render_text(result):
    lines = ['ADDITIONAL REASSESSMENT REPRODUCIBILITY SUPPLEMENT V2 PUBLIC DERIVATIVE',
             'Author approved 10 October 2026; public packaging candidate; calculation-only verification.',
             'The result remains conditional on assessor judgments and retained Stage 2 inputs.',
             'Evidence and coding validity are NOT independently validated. Stage 3 remains unapproved.',
             'Condition order: ' + ', '.join(CONDITIONS),
             'Unchanged rule: any U => Fail; otherwise all S => Pass; otherwise Unresolved.',
             'Original ZIP SHA-256: ' + result['provenance']['original_supplement_sha256'], '']
    calculations = result['calculations']
    groups = calculations['unchanged_historical_comparisons'] + [calculations['additional_reassessment']] + calculations['single_U_counterfactuals']
    for group in groups:
        lines += [group['group_id'], 'Status: ' + group['status']]
        for case in group['cases']:
            lines.append('  ' + case['name'] + ': ' + '/'.join(case['possible_results']) + '; assignments=' + str(case['alternative_count']))
            for variant in case['alternatives']:
                cells = variant['decisive_U_cells'] if variant['result'] == 'Fail' else variant['unresolved_blocking_cells']
                label = 'decisive U' if variant['result'] == 'Fail' else 'unresolved blockers' if variant['result'] == 'Unresolved' else 'all S'
                lines.append('    ' + '/'.join(variant['states']) + ' => ' + variant['result'] + '; ' + label + ': ' + ', '.join(c['condition'] + '=' + c['state'] for c in cells))
        lines.append('  Joint assignments: ' + str(group['joint_assignment_count']))
        lines.append('  Case-result vector invariant: ' + str(group['case_result_vector_invariant']))
        lines.append('  Totals: ' + json.dumps(group['possible_case_result_counts'], sort_keys=True))
        lines.append('  Cell-count ranges: ' + json.dumps(group['cell_state_count_ranges'], sort_keys=True))
        lines.append('')
    lines += ['DEPENDENCIES'] + ['- ' + x for x in result['dependencies']]
    lines += ['', 'SELF-TESTS: ' + result['self_tests']['status']]
    lines += ['- ' + json.dumps(x, sort_keys=True) for x in result['self_tests']['groups']]
    lines += ['', 'LIMITATIONS'] + ['- ' + x for x in result['limits']]
    return '\n'.join(lines) + '\n'


def verify_manifest(base):
    names = set()
    for line in (base / 'SHA256SUMS_PUBLIC.txt').read_text(encoding='utf-8').splitlines():
        expected, filename = line.split('  ', 1)
        safe_filename(filename)
        require(filename not in names, 'duplicate manifest entry')
        require(digest((base / filename).read_bytes()) == expected, 'file hash mismatch: ' + filename)
        names.add(filename)
    expected_files = {'README_PUBLIC.txt', 'check_additional_reassessment_public.py', 'recorded_inputs_public.json', 'results_public.json', 'results_public.txt', 'public_author_approval.json', 'additional_reassessment_source_snapshot.txt', 'Staged_Aggregation_Reproducibility_original.zip.b64', 'PUBLIC_PACKAGING_CHANGES.txt'}
    require(names == expected_files, 'manifest coverage mismatch')
    return len(names)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path(__file__).resolve().with_name('recorded_inputs_public.json'))
    parser.add_argument('--output-dir', type=Path, help='Default: input directory; writes results_public.json and results_public.txt only.')
    parser.add_argument('--verify-saved', action='store_true', help='Read-only recomputation, byte comparison and full manifest verification.')
    args = parser.parse_args()
    raw_input = args.input.read_bytes()
    data = json_read(raw_input)
    previous, saved = load_dependencies(data, args.input.parent)
    results = {'supplement_id': data['supplement_id'], 'status': 'PASS: mechanical reproduction only',
               'provenance': {'inputs_sha256': digest(raw_input), 'checker_sha256': digest(Path(__file__).read_bytes()),
                              'original_supplement_sha256': ORIGINAL_SHA256, 'original_inputs_sha256': data['previous_supplement']['recorded_inputs_sha256'],
                              'additional_source_sha256': data['additional_source']['sha256'], 'public_approval_statement_sha256': data['public_approval']['sha256'],
                              'author_approval_date': data['public_approval']['approval_date'], 'author': data['public_approval']['author']},
               'condition_order': data['condition_order'], 'aggregation_rule': data['aggregation_rule'],
               'dependencies': data['additional_reassessment']['dependencies'], 'self_tests': self_tests(data, previous, saved),
               'calculations': compute(data, previous), 'limits': data['limits']}
    outputs = {'results_public.json': json.dumps(results, ensure_ascii=False, indent=2) + '\n', 'results_public.txt': render_text(results)}
    dest = args.output_dir if args.output_dir is not None else args.input.parent
    if args.verify_saved:
        for name, content in outputs.items():
            require((dest / name).read_bytes() == content.encode('utf-8'), 'saved result mismatch: ' + name)
        count = verify_manifest(args.input.parent)
        print('PASS: saved results reproduced byte-for-byte; verified ' + str(count) + ' content-file hashes.')
    else:
        dest.mkdir(parents=True, exist_ok=True)
        for name, content in outputs.items():
            (dest / name).write_text(content, encoding='utf-8')
        print('PASS: wrote results_public.json and results_public.txt in ' + str(dest))
    group = results['calculations']['additional_reassessment']
    print('Additional joint assignments: ' + str(group['joint_assignment_count']))
    print('Possible totals: ' + json.dumps(group['possible_case_result_counts']))
    print('4^6 rule tests PASS. No evidence/state validation; Stage 3 remains unapproved.')


if __name__ == '__main__':
    try:
        main()
    except (InputError, ValueError, TypeError, KeyError, OSError, zipfile.BadZipFile) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        sys.exit(2)
