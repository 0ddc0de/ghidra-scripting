
## Setup

```
pip install -r requirements.txt
python -m ghidra_bridge.install_server ~/ghidra_scripts
```

## Run

Start ghidra bridge in one terminal:
```
<ghidra_root>/support/analyzeHeadless ~/ghidraproj bbcount -import <binary> -postScript ghidra_bridge_server.py -deleteProject
```

Run script in another terminal:
```
./countbb.py
```

Output is currently `/tmp/bb_breakpoints.yml`.

## Notes

* ghidra bridge is a terrible solution to iterate all basic blocks. Due to the round trips, the analysis takes forever.
