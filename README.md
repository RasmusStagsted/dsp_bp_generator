# dsp_bp_generator (Work in progress)

This is a small project to generate blueprint to the game Dyson Sphere Program (DSP).
The project is inspired from the awesome work put into [dspbptk](https://github.com/johndoe31415/dspbptk), from where the MD5 implementation and the DysonSphereItem enum is taken.

In the beginning, the project aimed to be a tool only to generate a production factory of a user defined item. But since then, it have evolved to be a more generic implementation of a library, to generate and connect various buildings, due to the complexity of the way the blue print is encoded.

## How to use

A few small examples show how to run the parser and the serializer of blueprints. As well as a small example of how to generate blueprints from scratch:

(tested using Python 3.8.10)

Create virtual environment:
```
python -m venv venv
```

Activate the virtual environment:
```
source venv/bin/activate
```

Install dependencies:
```
pip install -r requirements.txt
```

Install this package:
```
pip install .
```

To run the blueprint parser, save your blueprint in a file, and run: 
```
python parse.py --input_file=bp_input.txt --output_file=bp_output_data.txt
```

To run the blueprint parser- editer & serializer, save your blueprint in a file, and run:
```
python parse_edit_and_serialize.py --input_file=bp_input.txt --output_file=bp_output.txt
```

To generate and serialize a blueprint, try running:
```
python generate_and_serialize.py --output_file=bp_output.txt
```

## Blueprint encoding

A blueprint in Dyson Sphere Program is a list of binary data blobs, each representing a building (this protocol is derived from the awsome work done in [dspbptk](https://github.com/johndoe31415/dspbptk)).

<table>
<tr><th> Building </th><th> Pose </th><th> Connection </th></tr>
<tr><td valign="top">

| Name             | Type          |
|:---------------- |:-------------:|
| index            | int32         |
| area_index       | int8          |
| <b>pose          | <b>Pose       |
| item_id          | int16         |
| model_index      | int16         |
| <b>connection    | <b>Connection |
| recipe_id        | int16         |
| filter_id        | int16         |
| parameter_count  | int16         |
| parameters       | [int32]       |

</td><td valign="top">

| Name             | Type    |
|:---------------- |:-------:|
| x1               | float32 |
| y1               | float32 |
| z1               | float32 |
| x2               | float32 |
| y2               | float32 |
| z2               | float32 |
| yaw              | float32 |
| yaw2             | float32 |

</td><td valign="top">

| Name             | Type    |
|:---------------- |:-------:|
| output_index     | int32   |
| input_index      | int32   |
| output_to_slot   | int8    |
| input_from_slot  | int8    |
| output_from_slot | int8    |
| input_to_slot    | int8    |
| output_offset    | int8    |
| input_offset     | int8    |

</td></tr> </table>

All these field is used to specify settings for each single object. The simple ones are for instance the postions (some buildings have two positions such as Sorters), but more complex ones are the indicies, which can be linked together to specify for instance a connection between two Belts, or a connection from a Sorter to an Arc Smelter.
Small helper functions to handle all these settings for each building type have growned into a small library of tools to generate generic blueprints.

Before this big datablob, represnting a list of buildings, is a couple of headers.

<table>
<tr><th> Blueprint </th><th> Header </th><th> Area </th></tr>
<tr><td valign="top">

| Name             | Type          |
|:---------------- |:-------------:|
| <b>header        | <b>Header     |
| building_count   | int32         |
| <b>buildings     | <b>[Building] |

</td><td valign="top">

| Name               | Type      |
|:------------------ |:---------:|
| version            | int8      |
| cursor_offset_x    | int8      |
| cursor_offset_x    | int16     |
| cursor_target_area | int16     |
| dragbox_size_x     | int16     |
| dragbox_size_y     | int16     |
| primary_area_index | int16     |
| area_count         | int16     |
| <b>areas           | <b>[Area] |

</td><td valign="top">

| Name          | Type  |
|:------------- |:-----:|
| index         | int8  |
| parent_index  | int8  |
| tropic anchor | int16 |
| area segments | int16 |
| offset x      | int16 |
| offset y      | int16 |
| width         | int16 |
| height        | int16 |

</td></tr> </table>

This whole data blob is finnaly compressed using gzip and then base64 encoded.
Furthermore a fixed string is prepended, and a hash is appended.

### Bluepring structure

For now only the most basic features is implemented.
Generate and connects:
 - Belts
 - Smelters
 - Sorters
 - Assemblers
 - Splitters
 - Power poles

Forthermore, functionality to generate a production bus for an specific item at a user defined rate is implemented. However, only smelters and assemblers are supported. Which means no support for oil refinaries, chemical plants, etc.

![alt text](https://github.com/RasmusStagsted/dsp_bp_generator/blob/main/screenshot.png?raw=true)
The factory above is generated by dsp_bp_generator

## Limitations:
 - Do only support one recipe per item
 - Does only support smelter- and assembler factories
 - Does only support single output recipies
 - Does not (fully) support prolifirator (Mk.I, Mk.II, Mk.III)
 - Assumes all sorters and belts lives up to the requirements of throughput
 - Does not support multiple belts of same item
 - Does not support different tiers of sorters, factories nor belts
 - Documentation...

# TODOs
For now only the very basic support of structures are implemented.

Buildings to implement:
 * ~~Tesla Tower~~
 * Wireless Power Tower
 * Satelite Substation
 * Wind turbine
 * Thermal Power Plant
 * Solar Panel
 * Accumulator
 * Geothermal Power Station
 * Mini Fusion Power Plant
 * Energy Exchanger
 * Ray Receiver
 * ~~Conveyer Belt MK.I~~
 * ~~Conveyer Belt MK.II~~
 * ~~Conveyer Belt MK.III~~
 * ~~Splitter~~
 * Automatic Piler
 * Traffic Monitor
 * Spray Coater
 * Depot MK.I
 * Depot MK.II
 * Storange Tank
 * Logistic Distributor
 * Planeraty Logistics Station
 * Interstellar Logistic Station
 * Orbital Collector
 * ~~Sorter MK.I~~
 * ~~Sorter MK.II~~
 * ~~Sorter MK.III~~
 * ~~Pile Sorter~~
 * Mining Machine
 * Advanced Mining Machine
 * Water Pump
 * Oil Extractor
 * Oil Refinary
 * Fractionator
 * Chemical Plant
 * Quantum Chemical Plant
 * Miniature Particle Collider
 * ~~Arc Smelter~~
 * Plane Smelter
 * ~~Assembling Machine Mk.I~~
 * ~~Assembling Machine Mk.II~~
 * ~~Assembling Machine Mk.III~~
 * Matrix Lab
 * EM-Rail Ejector
 * Vertical Launching Silo
 * Gauss Turret
 * Missile Turret
 * Implosion cannon
 * Laser Turret
 * Plasma Turret
 * SR Plasma Turret
 * Battlefield Analysis Base
 * Jammer Tower
 * Signal Tower
 * Planetary Shield Generator