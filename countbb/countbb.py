#!/usr/bin/env python3
""" Save entry addresses of all basic blocks 
Based on https://github.com/HackOvert/GhidraSnippets#working-with-basic-blocks
"""
import ghidra_bridge
import yaml


def get_bbs(funcs, blockModel, monitor):
    """Returns a set of `func`'s bbs."""
    bbs = set()

    func_blocks = bridge.remote_eval(
        "[(func, blockModel.getCodeBlocksContaining(func.getBody(), monitor)) "
        "for func in funcs]",
        funcs=funcs,
        blockModel=blockModel,
        monitor=monitor,
    )

    for func, block in func_blocks:
        # add the entrypoint
        ep = func.getEntryPoint().getOffset()
        print(f"Processing func@{ep:#x}")
        bbs.add(ep)

        while block.hasNext():
            bb = block.next()
            dest = bb.getDestinations(monitor)
            while dest.hasNext():
                dbb = dest.next()
                # For some odd reason `getCodeBlocksContaining()` and `.next()`
                # return the root basic block after CALL instructions (x86).
                # To filter these out, we use `getFunctionAt()` which returns
                # `None` if the address is not the entry point of a function.
                # See:
                # https://github.com/NationalSecurityAgency/ghidra/issues/855
                if not getFunctionAt(dbb.getDestinationAddress()):
                    bbs.add(dbb.getSourceAddress().getOffset())
    return bbs


def main():
    ghidra.program.model.data.DataUtilities.isUndefinedData(
        currentProgram, currentAddress
    )
    funcs = currentProgram.getFunctionManager().getFunctions(True)
    monitor = ghidra.util.task.ConsoleTaskMonitor()
    blockModel = ghidra.program.model.block.BasicBlockModel(currentProgram)

    bbs = get_bbs(funcs, blockModel, monitor)

    bbs = list(bbs)
    fout = "/tmp/bbs.yml"
    with open(fout, "w") as f:
        yaml.dump({"bbs": bbs}, f)
    print(f"Output file: {fout}")


if __name__ == "__main__":
    global bridge
    bridge = ghidra_bridge.GhidraBridge(namespace=globals())
    main()
    # bridge.remote_shutdown()
