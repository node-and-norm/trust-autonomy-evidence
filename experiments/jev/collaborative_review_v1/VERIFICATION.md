# Preservation verification

The new credential-free verifier passed for all 24 approved records. Individual
bytes match their original hashes and consolidated entries; unit identities and
source request/response hashes match the pinned cohort. Items 8 and 16 retain
null classifications. Timing and benefit measurements remain null. A temporary
copy with item 8 changed to supported was rejected. No source record was changed.

Only this new preservation directory is included in the commit. Existing frozen
experiment files and scores are unchanged.

An additional replay of the earlier pilot results was attempted but not confirmed
in this session. The previous temporary Python environment was unavailable.
System Python 3.9 reported `Frozen analysis differs`; bundled Python 3.12 lacked
jsonschema. The cause of the 3.9 mismatch was not investigated in this preservation
task. These attempts are not reported as passing research-result reproduction.
The new preservation verifier uses only the Python standard library and passed.
