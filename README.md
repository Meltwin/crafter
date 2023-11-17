<h1 align="center">Crafter Analysis </h1>

This is a Minecraft's Crafter input / output rate analysis script.

This repository contains the script to analyse the flow rate of the Minecraft crafter.
Multiple parameters are available to test:

- The number of items for the craft
- The number of input (theoric max 6 = number of face, practicaly only 4 possible)
- The rate of the input channel (e.g. hopper, dropper, ...)
- The frequency of the clock

By Meltwin - 2023 under the MIT Licence

## Running it

To run this script, you'll need Python with the packages Numpy and Matplotlib installed. Then, you can run it with the command:

```shell
$ python3 crafter.py
```

## Testing other things

You can test any situation with this script. At the end of the file you will find the lines to configures what the script has to show:

```python
RT = lambda x: 2 * x  # RedstoneTicks
GT = lambda x: x  # GameTicks

HOPPER_MAX_TRSFRT = RT(4)  # GT/item
DROPPER_MAX_TRSFRT = RT(2)  # GT/item

test_params(
    [RT(1), GT(1), GT(0.5)],  # GT/impule
    [HOPPER_MAX_TRSFRT, DROPPER_MAX_TRSFRT, RT(1), GT(1)],
    ["Hopper", "Dropper", "1RT", "1GT"],
)
```

The function `test_params` takes as arguments:

- The clocks frequencies in game tick/impulse,
- The input flowrate as game tick/item
- The name of the associated input method
