"""Crafter input / output rate analysis script

This file contains the script to analyse the flow rate of the Minecraft crafter.
Multiple parameters are available to test:
- The number of items for the craft
- The number of input (theoric max 6 = number of face, practicaly only 4 possible)
- The rate of the input channel (e.g. hopper, dropper, ...)
- The frequency of the clock

By Meltwin - 2023
"""
from typing import Tuple, Generator
import matplotlib.pyplot as plt
from matplotlib.axis import Axis
import numpy as np

MAX_N_INPUT = [4, 6]
n_inputs = np.linspace(1, MAX_N_INPUT[1], MAX_N_INPUT[1])  # Number of inputs


def test_params(
    clock_values: list[float], input_trsfrt: list[float], input_names: list[str]
):
    fig, ax = plt.subplots(len(clock_values), len(input_trsfrt))
    fig.suptitle(
        "Input / Ouput analysis of the crafter \nBy Meltwin - 2023", fontsize=34
    )

    def next_params(
        axs, clock_list: list[float], input_list: list[float], input_name: list[str]
    ) -> Generator[Tuple[Axis, float, float, str, bool, bool], None, None]:
        for clock_idx in range(len(clock_list)):
            for input_idx in range(len(input_list)):
                if len(clock_list) == 1:
                    if len(input_list) == 1:
                        yield (
                            axs,
                            clock_list[clock_idx],
                            input_list[input_idx],
                            input_name[input_idx],
                            clock_idx,
                            input_idx,
                        )
                    else:
                        yield (
                            axs[input_idx],
                            clock_list[clock_idx],
                            input_list[input_idx],
                            input_name[input_idx],
                            clock_idx,
                            input_idx,
                        )
                else:
                    if len(input_list) == 1:
                        yield (
                            axs[clock_idx],
                            clock_list[clock_idx],
                            input_list[input_idx],
                            input_name[input_idx],
                            clock_idx,
                            input_idx,
                        )
                    else:
                        yield (
                            axs[clock_idx, input_idx],
                            clock_list[clock_idx],
                            input_list[input_idx],
                            input_name[input_idx],
                            clock_idx,
                            input_idx,
                        )

    for axis, clock, input_rate, input_name, clck_idx, input_idx in next_params(
        ax, clock_values, input_trsfrt, input_names
    ):
        # Draw interesting area
        axis.axhline(
            y=20 / input_rate,
            color="r",
            linestyle="--",
            linewidth=4,
            label="Max / channel",
        )
        axis.axvspan(
            MAX_N_INPUT[0],
            MAX_N_INPUT[1],
            alpha=0.15,
            color="green",
            label="Impossible input",
        )
        other_ax = axis.twinx()

        # Draw the different plots
        for n_items in range(1, 10):
            output_rate = (
                np.min(
                    np.vstack(
                        (
                            n_inputs / (input_rate * n_items),
                            np.ones((MAX_N_INPUT[1])) / clock,
                        )
                    ),
                    axis=0,
                )
                * 20
            )
            axis.plot(
                n_inputs,
                n_items * np.divide(output_rate, n_inputs),
                "--x",
                label=f"{n_items} items  / craft",
                linewidth=0.6,
            )
            other_ax.plot(
                n_inputs,
                output_rate,
                "-s",
                label=f"{n_items} items / craft",
                linewidth=1.2,
            )

        # Display the labels
        if clck_idx == len(clock_values) - 1:
            axis.set_xlabel("Number of input")
        if input_idx == 0:
            axis.set_ylabel("[Input] Item / s / channel")
        if input_idx == len(input_trsfrt) - 1:
            other_ax.set_ylabel("[Output] Item / s")

        # Setup the grid
        axis.grid(which="major", alpha=0.5, axis="y", linestyle=":")
        axis.grid(which="major", alpha=1, axis="x", linestyle="-")
        other_ax.grid(which="major", alpha=0.7)
        axis.set_xticks(n_inputs)

        axis.set_xlim([1, MAX_N_INPUT[1]])

        # Setup the legend
        if (input_idx == len(input_trsfrt) - 1) and (
            clck_idx == len(clock_values) // 2
        ):
            other_ax.legend(
                loc="center left",
                bbox_to_anchor=(1.2, 0.5),
                fancybox=True,
                shadow=True,
                title="Output curves",
            )
        if (input_idx == 0) and (clck_idx == len(clock_values) // 2):
            axis.legend(
                loc="center right",
                bbox_to_anchor=(-0.2, 0.5),
                fancybox=True,
                shadow=True,
                title="Input curves",
            )
        axis.set_title(f"Using {input_name} with a clock of {clock} GT/impulse")
    plt.show()


RT = lambda x: 2 * x  # RedstoneTicks
GT = lambda x: x  # GameTicks

HOPPER_MAX_TRSFRT = RT(4)  # GT/item
DROPPER_MAX_TRSFRT = RT(2)  # GT/item

test_params(
    [RT(1), GT(1), GT(0.5)],  # GT/impule
    [HOPPER_MAX_TRSFRT, DROPPER_MAX_TRSFRT, RT(1), GT(1)],
    ["Hopper", "Dropper", "1RT", "1GT"],
)
