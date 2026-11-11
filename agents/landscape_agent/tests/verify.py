"""Independent structural checks; content flags are coverage checks, not proof of reasoning."""
import hashlib,json,subprocess,sys
from pathlib import Path
import jsonschema
root=Path(__file__).resolve().parents[3]
a=root/'agents/landscape_agent'
rows=[]
def command(args):
 r=subprocess.run([sys.executable,*map(str,args)],text=True,capture_output=True)
 return {'exit_code':r.returncode,'stdout':r.stdout.strip(),'stderr':r.stderr.strip()}
validator=jsonschema.Draft202012Validator(json.loads((root/'core/output_schema.json').read_text()))
intake=jsonschema.Draft202012Validator(json.loads((root/'core/input_schema.json').read_text()))
for case in ['primary','contrast_1','contrast_2']:
 intake.validate(json.loads((a/f'cases/{case}.json').read_text()))
for name in ['v01_primary','primary','contrast_1','contrast_2']:
 path=a/f'responses/{name}_response.json';d=json.loads(path.read_text())
 errors=[e.message for e in validator.iter_errors(d)]
 r={'run':name,'instructor_validator':command([root/'tools/validate_response.py',path]),'strict_schema_errors':errors,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
 rows.append(r)
assert all(r['instructor_validator']['exit_code']==0 and not r['strict_schema_errors'] for r in rows)
# Counterexample: demonstrate why the second validator is needed, without fabricating a model failure.
probe=json.loads((a/'responses/primary_response.json').read_text());probe['unrequested_field']='schema-probe'
probe_path=a/'tests/extra_field_probe.json';probe_path.write_text(json.dumps(probe,indent=2))
probe_result=command([root/'tools/validate_response.py',probe_path]);strict_probe=list(validator.iter_errors(probe))
assert probe_result['exit_code']==0 and strict_probe
stable=[json.loads((a/f'responses/{n}_response.json').read_text())['general_et_finding'] for n in ['primary','contrast_1','contrast_2']]
assert len(set(stable))==1
context=[json.loads((a/f'responses/{n}_response.json').read_text())['organization_specific_finding'] for n in ['primary','contrast_1','contrast_2']]
assert len(set(context))==3
integrity=command([root/'tools/check_frozen_core.py']);assert integrity['exit_code']==0
report={'verification_date':'2026-11-10 America/New_York','method':'Python instructor validator plus jsonschema Draft202012Validator; same-session qualitative review is separate','cases':'3 valid inputs; 4 model responses (v0.1 primary plus v0.2 primary and two contrasts)','results':rows,'negative_control':{'origin':'Constructed validator diagnostic, NOT a model output or model execution','instructor_accepts_extra_property':probe_result['exit_code']==0,'strict_rejects_extra_property':bool(strict_probe),'errors':[e.message for e in strict_probe]},'general_finding_stability':'PASS exact text equality; appropriateness requires qualitative review','context_distinction':'PASS different strings; meaning assessed separately','frozen_core':integrity}
(a/'records/validation_results.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
