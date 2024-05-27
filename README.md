# dsp_bp_generator (Work in progress)

## Dyson Sphere Program blueprint generator

This is a small project trying to generate blueprint to the game Dyson Sphere Program (DSP).
The project is inspired from dspbptk, from where the MD5 implementation and the DysonSphereItem enum is taken.

For now only the most basic features is implemented.
Generate and connects:
 - Belts
 - Smelters
 - Sorters
 - Assemblers
 - Splitters
 - Power poles

Forthermore, functionality to generate a production bus for an specific item at a user defined rate is implemented. However, only smelters and assemblers are supported. Which means no support for oil refinaries, chemical plants, etc.

## Limitations:
 - Does only support smelter- and assembler factories
 - Does only support single output recipies
 - Does not (fully) support prolifirator (Mk.I, Mk.II, Mk.III)
 - Assumes all sorters and belts lives up to the requirements of throughput
 - Does not support multiple belts of same item
 - Does not support different tiers of sorters, factories nor belts
 - Documentation...

## More planned features:
 - GUI
 - Support of logistics stations
