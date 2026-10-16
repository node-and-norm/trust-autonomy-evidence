"""Offline, standard-library-only reproduction of recorded categorical states.

This program checks aggregation and input transcription, not the truth of the
states or evidence. It never contacts a network or changes the source inputs.
"""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path
import re
import sys

CONDITIONS = ['access', 'comprehension', 'authority', 'feasibility', 'exercise', 'propagation']
STATES = ('S', 'P', 'U', 'I')
RESULTS = ('Pass', 'Fail', 'Unresolved')
RULE = {'priority': ['any_U', 'all_S', 'otherwise_P_or_I'], 'any_U': 'Fail',
        'all_S': 'Pass', 'otherwise_P_or_I': 'Unresolved',
        'change_from_released_rule': 'none'}


class InputError(ValueError):
    """A malformed or internally inconsistent recorded input."""


def require(condition, message):
    if not condition:
        raise InputError(message)


def fields(obj, names, where):
    require(type(obj) is dict, where + ': must be an object')
    expected = set(names.split())
    require(set(obj) == expected, where + ': missing or unexpected fields: ' +
            repr(sorted(set(obj) ^ expected)))


def nonempty(value, where):
    require(type(value) is str and bool(value.strip()), where + ': must be a nonempty string')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def reject_duplicate_keys(pairs):
    obj = {}
    for key, value in pairs:
        require(key not in obj, 'duplicate JSON key: ' + key)
        obj[key] = value
    return obj


def load_json(path):
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=reject_duplicate_keys)


def state_options(cell, where):
    options = [cell] if type(cell) is str else cell
    require(type(options) is list and bool(options), where + ': state or nonempty state-set required')
    require(all(type(s) is str and s in STATES for s in options), where + ': invalid state')
    require(len(options) == len(set(options)), where + ': repeated alternative')
    return options


def parse_expression(expression):
    nonempty(expression, 'source_state_expression')
    parts = expression.split('/')
    require(len(parts) == 6, 'source expression must contain six slash-separated cells')
    parsed = []
    for part in parts:
        part = part.strip()
        if part.startswith('{') and part.endswith('}'):
            parsed.append(state_options([x.strip() for x in part[1:-1].split(',')], 'source expression'))
        else:
            parsed.append(state_options(part, 'source expression'))
    return parsed


def aggregate(row):
    require(type(row) in (list, tuple) and len(row) == 6, 'row must contain exactly six states')
    require(all(type(s) is str and s in STATES for s in row), 'row contains an invalid/missing state')
    if 'U' in row:
        return 'Fail'
    if all(s == 'S' for s in row):
        return 'Pass'
    return 'Unresolved'


def validate(data, ledger):
    fields(data, 'schema_version purpose scope source baseline condition_order historical_field_aliases aggregation_rule cases stages propagation_only_diagnostic rule_illustrations limitations', 'input')
    require(type(data['schema_version']) is int and data['schema_version'] == 1, 'unsupported schema_version')
    for key in ('purpose', 'scope'):
        nonempty(data[key], key)
    fields(data['source'], 'file sha256 description', 'source')
    nonempty(data['source']['description'], 'source.description')
    require(type(data['source']['file']) is str and Path(data['source']['file']).name == data['source']['file'] and data['source']['file'] not in ('.', '..'), 'source.file must be a local basename')
    require(type(data['source']['sha256']) is str and re.fullmatch('[0-9a-f]{64}', data['source']['sha256']) is not None, 'invalid source SHA-256')
    fields(data['baseline'], 'version commit evidence_cutoff aggregation_introduced', 'baseline')
    for key, value in data['baseline'].items():
        nonempty(value, 'baseline.' + key)
    require(re.fullmatch('[0-9a-f]{40}', data['baseline']['commit']) is not None, 'invalid baseline commit')
    require(data['condition_order'] == CONDITIONS, 'condition_order must match the fixed six-condition order')
    require(data['historical_field_aliases'] == {'propagation': 'effect'}, 'historical effect/propagation alias changed')
    require(data['aggregation_rule'] == RULE, 'aggregation rule or priority changed')
    require(type(data['cases']) is list and len(data['cases']) == 3, 'exactly three case identities required')
    case_ids = []
    for case in data['cases']:
        fields(case, 'case_id name baseline_path baseline_git_blob', 'case')
        for key, value in case.items():
            nonempty(value, 'case.' + key)
        require(re.fullmatch('[0-9a-f]{40}', case['baseline_git_blob']) is not None, 'invalid case Git blob')
        case_ids.append(case['case_id'])
    require(len(set(case_ids)) == 3, 'duplicate case identity')
    require(type(data['stages']) is list and len(data['stages']) == 3, 'exactly three main stages required')
    expected_statuses = [('stage_1', 'released_historical', 'historical_record'),
                         ('stage_2', 'conditional_state_sets', 'pending'),
                         ('stage_3', 'conditional_unadopted', 'pending')]
    for stage, status in zip(data['stages'], expected_statuses):
        fields(stage, 'stage_id title status author_approval source_section interpretation rows', 'stage')
        require((stage['stage_id'], stage['status'], stage['author_approval']) == status, 'stage identity/status/adoption changed')
        for key in ('title', 'source_section', 'interpretation'):
            nonempty(stage[key], 'stage.' + key)
        require(stage['source_section'] in ledger, 'source section absent from ledger')
        require(type(stage['rows']) is list and len(stage['rows']) == 3, 'three case rows required for each stage')
        row_ids = []
        for row in stage['rows']:
            fields(row, 'case_id states source_state_expression source_quote', 'stage row')
            row_ids.append(row['case_id'])
            require(type(row['states']) is list and len(row['states']) == 6, 'six required condition cells must be present')
            actual = [state_options(x, 'stage state') for x in row['states']]
            require(actual == parse_expression(row['source_state_expression']), 'state cells do not match recorded source expression')
            nonempty(row['source_quote'], 'source_quote')
            require(row['source_quote'] in ledger, 'source quote absent from ledger')
            require(row['source_state_expression'] in row['source_quote'], 'source expression absent from source quote')
            if stage['stage_id'] != 'stage_2':
                require(all(len(x) == 1 for x in actual), 'only Stage 2 contains main-stage state alternatives')
        require(row_ids == case_ids, 'case row identity/order mismatch')
    diag = data['propagation_only_diagnostic']
    fields(diag, 'diagnostic_id base_stage condition case_ids allowed_replacements label source_section', 'diagnostic')
    require(diag['diagnostic_id'] == 'propagation_only' and diag['base_stage'] == 'stage_1', 'invalid diagnostic identity/base')
    require(diag['condition'] == 'propagation', 'propagation-only diagnostic changed condition')
    require(type(diag['case_ids']) is list and len(diag['case_ids']) == 2 and len(set(diag['case_ids'])) == 2 and all(x in case_ids for x in diag['case_ids']), 'invalid diagnostic case identities')
    require(diag['allowed_replacements'] == ['S', 'P', 'I'], 'diagnostic must enumerate all three non-U replacements')
    nonempty(diag['label'], 'diagnostic.label')
    require(type(diag['source_section']) is str and diag['source_section'] in ledger, 'diagnostic source section absent')
    illustrations = data['rule_illustrations']
    require(type(illustrations) is list and len(illustrations) == 3, 'three single-U rule illustrations required')
    illustration_ids, changed = [], []
    for item in illustrations:
        fields(item, 'illustration_id base_stage case_id condition replacement label', 'rule illustration')
        nonempty(item['illustration_id'], 'illustration_id')
        nonempty(item['label'], 'illustration.label')
        require(item['base_stage'] == 'stage_3', 'rule illustration must start from full conditional proposal')
        require(item['case_id'] in case_ids, 'unknown illustration case')
        require(item['replacement'] == 'U', 'single-U illustration must insert U')
        illustration_ids.append(item['illustration_id'])
        changed.append(item['condition'])
    require(len(set(illustration_ids)) == 3 and sorted(changed) == ['comprehension', 'exercise', 'feasibility'], 'invalid illustration identities/conditions')
    require(type(data['limitations']) is list and bool(data['limitations']), 'limitations must be a nonempty list')
    for limitation in data['limitations']:
        nonempty(limitation, 'limitation')


def explain(row):
    outcome = aggregate(row)
    u_cells = [{'condition': c, 'state': s} for c, s in zip(CONDITIONS, row) if s == 'U']
    unknowns = [{'condition': c, 'state': s} for c, s in zip(CONDITIONS, row) if s in ('P', 'I')]
    return {'states': list(row), 'result': outcome,
            'state_counts': {s: row.count(s) for s in STATES},
            'decisive_U_cells': u_cells,
            'unresolved_blocking_cells': unknowns if outcome == 'Unresolved' else [],
            'nondecisive_P_I_cells_when_Fail': unknowns if outcome == 'Fail' else [],
            'reason': ('Any U is sufficient for Fail; P/I elsewhere cannot override it.' if outcome == 'Fail' else
                       'All six states are S.' if outcome == 'Pass' else
                       'No U is present; the listed P/I cells prevent an all-S Pass.')}


def evaluate_group(group, case_names):
    output = {key: copy.deepcopy(value) for key, value in group.items() if key != 'rows'}
    case_results = []
    for row in group['rows']:
        alternatives = [state_options(cell, 'cell') for cell in row['states']]
        variants = []
        for number, states in enumerate(itertools.product(*alternatives), 1):
            variants.append({'variant_id': number, **explain(list(states))})
        result_set = [r for r in RESULTS if any(x['result'] == r for x in variants)]
        case_results.append({'case_id': row['case_id'], 'case_name': case_names[row['case_id']],
                             'recorded_state_cells': row['states'], 'alternative_count': len(variants),
                             'aggregate_invariant': len(result_set) == 1,
                             'possible_results': result_set, 'alternatives': variants})
    joint = []
    for number, combination in enumerate(itertools.product(*(x['alternatives'] for x in case_results)), 1):
        joint.append({'combination_id': number,
                      'case_variant_ids': {case['case_id']: variant['variant_id'] for case, variant in zip(case_results, combination)},
                      'case_results': {case['case_id']: variant['result'] for case, variant in zip(case_results, combination)},
                      'case_result_counts': {r: sum(v['result'] == r for v in combination) for r in RESULTS},
                      'cell_state_counts': {s: sum(v['state_counts'][s] for v in combination) for s in STATES}})
    signatures = sorted(set(tuple(j['case_result_counts'][r] for r in RESULTS) for j in joint))
    vectors = {tuple(j['case_results'][c['case_id']] for c in case_results) for j in joint}
    output.update({'cases': case_results, 'joint_assignment_count': len(joint),
                   'case_result_vector_invariant': len(vectors) == 1,
                   'case_result_counts_invariant': len(signatures) == 1,
                   'possible_case_result_counts': [dict(zip(RESULTS, x)) for x in signatures],
                   'cell_state_count_ranges': {s: {'min': min(j['cell_state_counts'][s] for j in joint), 'max': max(j['cell_state_counts'][s] for j in joint)} for s in STATES},
                   'joint_assignments': joint})
    return output


def compute(data):
    names = {case['case_id']: case['name'] for case in data['cases']}
    stages = {stage['stage_id']: stage for stage in data['stages']}
    main = [evaluate_group(stage, names) for stage in data['stages']]
    diag = data['propagation_only_diagnostic']
    group = copy.deepcopy(stages[diag['base_stage']])
    group.update({'stage_id': diag['diagnostic_id'], 'title': 'Propagation-only diagnostic',
                  'status': 'aggregation_only_not_adopted', 'author_approval': 'not_applicable',
                  'interpretation': diag['label'], 'source_section': diag['source_section']})
    for row in group['rows']:
        if row['case_id'] in diag['case_ids']:
            row['states'][CONDITIONS.index(diag['condition'])] = diag['allowed_replacements'][:]
    diagnostic = evaluate_group(group, names)
    illustrations = []
    for item in data['rule_illustrations']:
        group = copy.deepcopy(stages[item['base_stage']])
        group.update({'stage_id': item['illustration_id'], 'title': item['condition'] + ': counterfactual single-U rule illustration',
                      'status': 'rule_illustration_not_adopted', 'author_approval': 'not_applicable',
                      'interpretation': item['label']})
        for row in group['rows']:
            if row['case_id'] == item['case_id']:
                row['states'][CONDITIONS.index(item['condition'])] = item['replacement']
        illustrations.append(evaluate_group(group, names))
    return {'main_stages': main, 'propagation_only_diagnostic': diagnostic,
            'single_U_rule_illustrations': illustrations}


def self_tests(data, ledger):
    checks = []
    def check(condition, label):
        if not condition:
            raise RuntimeError('SELF-TEST FAILED: ' + label)
    counts = {r: 0 for r in RESULTS}
    for states in itertools.product(STATES, repeat=6):
        result = aggregate(states)
        # Independent decision specification expressed as counts and predicates.
        check((result == 'Fail') == (states.count('U') > 0), 'exhaustive U dominance')
        check((result == 'Pass') == (states.count('S') == 6), 'exhaustive all-S')
        check((result == 'Unresolved') == (states.count('U') == 0 and states.count('S') < 6), 'exhaustive unknown rule')
        counts[result] += 1
    check(counts == {'Pass': 1, 'Fail': 3367, 'Unresolved': 728}, 'exhaustive counts')
    checks.append({'name': 'all_4_to_the_6_valid_rows', 'passed': True, 'rows': 4096, 'result_counts': counts})
    explicit_dominance = 0
    for position in range(6):
        for other_states in itertools.product(('S', 'P', 'I'), repeat=5):
            row = list(other_states)
            row.insert(position, 'U')
            check(aggregate(row) == 'Fail', 'single-U dominates all five other states')
            check(not explain(row)['unresolved_blocking_cells'], 'Fail never attributed to an unknown blocker')
            explicit_dominance += 1
    checks.append({'name': 'explicit_single_U_dominance', 'passed': True, 'rows': explicit_dominance})
    check(aggregate(['S'] * 6) == 'Pass', 'explicit all-S')
    unknown_cases = 0
    for position in range(6):
        for state in ('P', 'I'):
            row = ['S'] * 6
            row[position] = state
            check(aggregate(row) == 'Unresolved', 'one P/I without U')
            check(len(explain(row)['unresolved_blocking_cells']) == 1, 'exact unresolved blocker')
            unknown_cases += 1
    checks.append({'name': 'explicit_all_S_and_unknown_cases', 'passed': True, 'all_S_rows': 1, 'single_unknown_rows': unknown_cases})
    invalid_rows = [None, 'SSSSSS', [], ['S'] * 5, ['S'] * 7]
    for invalid_state in (None, '', 'X', 's', 'P/I', ['P', 'I'], 0, True, {}):
        invalid_rows.append(['S', 'S', invalid_state, 'S', 'S', 'S'])
    for row in invalid_rows:
        try:
            aggregate(row)
        except InputError:
            pass
        else:
            raise RuntimeError('SELF-TEST FAILED: invalid row accepted: ' + repr(row))
    checks.append({'name': 'invalid_or_missing_state_rejection', 'passed': True, 'rejections': len(invalid_rows)})
    # Remove every object field in turn, including nested provenance and metadata.
    paths = []
    def visit(value, path):
        if type(value) is dict:
            for key, child in value.items():
                paths.append(path + [key])
                visit(child, path + [key])
        elif type(value) is list:
            for index, child in enumerate(value):
                visit(child, path + [index])
    visit(data, [])
    rejected = 0
    for path in paths:
        mutation = copy.deepcopy(data)
        target = mutation
        for part in path[:-1]:
            target = target[part]
        del target[path[-1]]
        try:
            validate(mutation, ledger)
        except (InputError, TypeError):
            rejected += 1
        else:
            raise RuntimeError('SELF-TEST FAILED: missing input field accepted: ' + repr(path))
    mutations = []
    def mutate(path, value):
        changed = copy.deepcopy(data)
        target = changed
        for part in path[:-1]:
            target = target[part]
        target[path[-1]] = value
        mutations.append(changed)
    mutate(['unexpected'], 1)
    mutate(['schema_version'], True)
    mutate(['condition_order'], list(reversed(CONDITIONS)))
    mutate(['aggregation_rule', 'priority'], ['all_S', 'otherwise_P_or_I', 'any_U'])
    mutate(['source', 'file'], '../outside.txt')
    mutate(['source', 'sha256'], 'bad-hash')
    mutate(['cases', 1, 'case_id'], data['cases'][0]['case_id'])
    mutate(['stages', 2, 'author_approval'], 'approved')
    mutate(['stages', 0, 'rows', 0, 'states'], ['P'] * 5)
    mutate(['stages', 0, 'rows', 0, 'states'], ['P'] * 5 + ['X'])
    mutate(['stages', 0, 'rows', 0, 'source_quote'], 'Not in the ledger')
    mutate(['stages', 0, 'rows', 0, 'states'], ['S'] * 6)
    mutate(['stages', 1, 'rows', 1, 'states', 2], [])
    mutate(['stages', 1, 'rows', 1, 'states', 2], ['P', 'P'])
    mutate(['propagation_only_diagnostic', 'allowed_replacements'], ['S', 'P', 'U', 'I'])
    mutate(['rule_illustrations', 0, 'replacement'], 'P')
    for changed in mutations:
        try:
            validate(changed, ledger)
        except (InputError, TypeError):
            pass
        else:
            raise RuntimeError('SELF-TEST FAILED: invalid input mutation accepted')
    try:
        json.loads('{"state":"S","state":"U"}', object_pairs_hook=reject_duplicate_keys)
    except InputError:
        pass
    else:
        raise RuntimeError('SELF-TEST FAILED: duplicate JSON key accepted')
    checks.append({'name': 'input_field_validation', 'passed': True,
                   'missing_field_rejections': rejected, 'invalid_input_rejections': len(mutations),
                   'duplicate_JSON_key_rejections': 1})
    # Deliberately mutate only an in-memory row, bypassing transcription validation.
    # Its result must change. This guards against hard-coded per-case results.
    probe = copy.deepcopy(data)
    probe['stages'][0]['rows'][0]['states'] = ['S'] * 6
    check(compute(probe)['main_stages'][0]['cases'][0]['possible_results'] == ['Pass'], 'computed outputs depend on states')
    probe['stages'][0]['rows'][0]['states'][0] = 'U'
    check(compute(probe)['main_stages'][0]['cases'][0]['possible_results'] == ['Fail'], 'computed U is not hard-coded')
    checks.append({'name': 'input_driven_computation', 'passed': True, 'in_memory_mutations': 2})
    calculated = compute(data)
    for group in calculated['single_U_rule_illustrations']:
        fail_rows = [case for case in group['cases'] if case['possible_results'] == ['Fail']]
        check(len(fail_rows) == 1, 'counterfactual inserts one failing case')
        row = fail_rows[0]['alternatives'][0]
        check(row['state_counts']['U'] == 1 and len(row['decisive_U_cells']) == 1, 'counterfactual contains exactly one decisive U')
        check(not row['unresolved_blocking_cells'], 'counterfactual unknowns do not override U')
    checks.append({'name': 'three_labeled_ZG710_single_U_counterfactuals', 'passed': True, 'illustrations': 3})
    return {'status': 'PASS', 'test_groups': checks}


def render_text(results):
    lines = ['STAGED AGGREGATION: MECHANICAL REPRODUCTION',
             'This checks recorded labels, not the evidence or the validity of those labels.',
             'Stage 3 is conditional and unadopted; historical assessments remain unchanged.',
             'Order: ' + ', '.join(CONDITIONS),
             'Rule: any U => Fail; otherwise all S => Pass; otherwise P/I => Unresolved.',
             'Input SHA-256: ' + results['provenance']['inputs_sha256'],
             'Ledger SHA-256: ' + results['provenance']['ledger_sha256'], '']
    groups = results['calculations']['main_stages'] + [results['calculations']['propagation_only_diagnostic']] + results['calculations']['single_U_rule_illustrations']
    for group in groups:
        lines += [group['title'], 'Status: ' + group['status'], group['interpretation']]
        for case in group['cases']:
            lines.append('  ' + case['case_name'] + ': ' + ' / '.join(case['possible_results']) +
                         '; ' + str(case['alternative_count']) + ' assignment(s); invariant=' + str(case['aggregate_invariant']))
            for variant in case['alternatives']:
                cells = variant['decisive_U_cells'] or variant['unresolved_blocking_cells']
                label = 'decisive U cells' if variant['result'] == 'Fail' else 'unresolved blockers' if variant['result'] == 'Unresolved' else 'all six S'
                named = ', '.join(x['condition'] + '=' + x['state'] for x in cells)
                lines.append('    ' + '/'.join(variant['states']) + ' => ' + variant['result'] + '; ' + label + (': ' + named if named else ''))
        lines.append('  Joint assignments enumerated: ' + str(group['joint_assignment_count']))
        lines.append('  Case-result vector invariant: ' + str(group['case_result_vector_invariant']))
        lines.append('  Possible totals: ' + '; '.join(', '.join(str(t[r]) + ' ' + r for r in RESULTS) for t in group['possible_case_result_counts']))
        lines.append('  Cell-count ranges: ' + ', '.join(s + '=' + str(v['min']) + ('..' + str(v['max']) if v['min'] != v['max'] else '') for s, v in group['cell_state_count_ranges'].items()))
        lines.append('')
    lines += ['SELF-TESTS: ' + results['self_tests']['status']]
    for test in results['self_tests']['test_groups']:
        lines.append('  ' + test['name'] + ': PASS; ' + json.dumps({k: v for k, v in test.items() if k not in ('name', 'passed')}, sort_keys=True))
    lines += ['', 'LIMITATIONS'] + ['  ' + x for x in results['limitations']]
    return '\n'.join(lines) + '\n'


def verify_manifest(base):
    manifest = base / 'SHA256SUMS.txt'
    require(manifest.is_file(), 'SHA256SUMS.txt is missing')
    entries = []
    for line in manifest.read_text(encoding='utf-8').splitlines():
        expected, filename = line.split('  ', 1)
        require(Path(filename).name == filename, 'manifest entries must be local basenames')
        require(filename not in entries, 'duplicate manifest filename')
        require(digest(base / filename) == expected, 'manifest hash mismatch: ' + filename)
        entries.append(filename)
    required = {'check_staged_aggregation.py', 'recorded_inputs.json', 'author_case_derivation_ledger.txt', 'README.txt', 'results.json', 'results.txt'}
    require(set(entries) == required, 'manifest does not cover the complete six-file package')
    return len(entries)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, default=Path(__file__).resolve().with_name('recorded_inputs.json'))
    parser.add_argument('--output-dir', type=Path, help='Default: input file directory; writes results.json/results.txt only.')
    parser.add_argument('--verify-saved', action='store_true', help='Read-only: recompute and byte-compare saved results; verify all package hashes.')
    args = parser.parse_args()
    data = load_json(args.input)
    require(type(data) is dict and type(data.get('source')) is dict and type(data['source'].get('file')) is str, 'missing source file field')
    filename = data['source']['file']
    require(Path(filename).name == filename and filename not in ('.', '..'), 'source.file must be a local basename')
    source_path = args.input.parent / filename
    ledger = source_path.read_text(encoding='utf-8')
    validate(data, ledger)
    require(digest(source_path) == data['source']['sha256'], 'ledger SHA-256 mismatch')
    results = {'status': 'PASS: mechanical checks only',
               'provenance': {'inputs_file': args.input.name, 'inputs_sha256': digest(args.input),
                              'ledger_file': source_path.name, 'ledger_sha256': digest(source_path),
                              'checker_file': Path(__file__).name, 'checker_sha256': digest(Path(__file__))},
               'condition_order': data['condition_order'], 'aggregation_rule': data['aggregation_rule'],
               'self_tests': self_tests(data, ledger), 'calculations': compute(data), 'limitations': data['limitations']}
    outputs = {'results.json': json.dumps(results, ensure_ascii=False, indent=2) + '\n', 'results.txt': render_text(results)}
    target = args.output_dir if args.output_dir is not None else args.input.parent
    if args.verify_saved:
        for filename, content in outputs.items():
            require((target / filename).read_bytes() == content.encode('utf-8'), 'saved output mismatch: ' + filename)
        count = verify_manifest(args.input.parent)
        print('PASS: reproduced saved results byte-for-byte; verified ' + str(count) + ' file hashes.')
    else:
        target.mkdir(parents=True, exist_ok=True)
        for filename, content in outputs.items():
            (target / filename).write_text(content, encoding='utf-8')
        print('PASS: wrote ' + str(target / 'results.json') + ' and ' + str(target / 'results.txt'))
    print('All 4^6 = 4096 rows passed. This does not validate the evidence or recorded states.')
    for group in results['calculations']['main_stages']:
        totals = group['possible_case_result_counts']
        print(group['stage_id'] + ': ' + json.dumps(totals) + '; joint assignments=' + str(group['joint_assignment_count']))


if __name__ == '__main__':
    try:
        main()
    except (InputError, OSError, ValueError, TypeError) as error:
        print('ERROR: ' + str(error), file=sys.stderr)
        sys.exit(2)
