"""
Copyright (c) 2024 MPI-M, Clara Bayley

-----  PerformanceTestingCLEO -----
File: read_kp_profilers.py
Project: profilers
Created Date: Monday 24th June 2024
Author: Clara Bayley (CB)
Additional Contributors:
-----
Last Modified: Monday 24th June 2024
Modified By: CB
-----
License: BSD 3-Clause "New" or "Revised" License
https://opensource.org/licenses/BSD-3-Clause
-----
File Description:
Functions to post-process output of Kokkos profilers to convert it into zarr datasets
"""


def file_to_lines(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
    return lines


def sections_from_lines(lines, seperator):
    start_anew_section = False
    current_section = []
    sections = []
    for line in lines:
        line = line.strip()
        if seperator in line:
            start_anew_section = True
        if start_anew_section:
            sections.append(current_section)
            current_section = []
            start_anew_section = False
        else:
            if line:
                current_section.append(line)
    if current_section:
        sections.append(current_section)

    return sections


def extract_between_lines(lines, start_line, end_line):
    if start_line not in lines or end_line not in lines:
        return []
    start = lines.index(start_line) + 1
    end = lines.index(end_line)
    return lines[start:end]


def kernel_timers_dataset(name, section):
    import xarray as xr

    def decode_kernel_timer(data):
        return {
            k: (
                ("timer"),
                v[1:],
                {
                    "type": v[0],
                    "columns": "Total Time, "
                    + "Call Count, "
                    + "Avg. Time per Call, "
                    + "%Total Time in Kernels, "
                    + "%Total Program Time",
                    "units": "s, [], s, %, %",
                },
            )
            for k, v in data.items()
        }

    data = {}
    for lnum in range(len(section) - 1):
        line = section[lnum]
        if line.split()[0] == "-" and len(line.split()) == 2:
            data_line = section[lnum + 1].split()
            values = [data_line[0]]
            values += list(map(float, data_line[1:]))
            data[line.split()[1]] = values

    ds = xr.Dataset(
        {k: v for k, v in decode_kernel_timer(data).items()},
        coords={
            "timer": [
                "time",
                "num_calls",
                "time_per_call",
                "percent_time_in_kernels",
                "percent_time_of_total",
            ],
        },
        attrs={"name": name},
    )
    return ds


def kernel_timers_summary_dataset(name, section):
    import xarray as xr

    data = []
    for line in section[1:-1]:
        data.append(float(line.split()[-2]))
    data.append(float(section[-1].split()[-1]))

    ds = xr.Dataset(
        {
            "summary": (
                ("summed_timer"),
                data,
                {
                    "columns": "Total Execution Time, "
                    + "Time in Kokkos kernels, "
                    + "Time outside Kokkos kernels, "
                    + "Percentage in Kokkos kernels, "
                    + "Calls to Kokkos Kernels",
                    "units": "s, s, s, %, []",
                },
            ),
        },
        coords={
            "summed_timer": [
                "total_time",
                "time_in_kernels",
                "time_out_kernels",
                "percent_time_in_kernels",
                "num_kernel_calls",
            ],
        },
        attrs={"name": name},
    )
    return ds


def kp_kernel_timer_datasets(sections):
    datasets = []
    for section in sections:
        if "Regions:" == section[0] or "Kernels:" == section[0]:
            name = section[0][:-1]  # excludes ':'
            datasets.append(kernel_timers_dataset(name, section))
        elif "Summary:" == section[0]:
            name = section[0][:-1]
            datasets.append(kernel_timers_summary_dataset(name, section))
    return datasets


def space_time_stack_allocations_dataset(name, section):
    import xarray as xr

    def decode_allocations(data):
        alloc_val = ":".join([s.split()[0][:-1] for s in section[2:]])
        alloc_name = ":".join([s.split()[-1] for s in section[2:]])
        return {
            "max_memory_allocation": (
                (),
                float(section[0].split()[-2]),
                {
                    "units": "kB",
                },
            ),
            "high_water_allocations": (
                (),
                alloc_val,
                {
                    "names": alloc_name,
                    "units": "%:%:%",
                },
            ),
        }

    ds = xr.Dataset(
        {k: v for k, v in decode_allocations(section).items()},
        attrs={"name": name},
    )
    return ds


def combine_space_time_stack_allocations_dataset(datasets):
    import xarray as xr

    dataset = xr.concat(datasets, dim="spaces")
    dataset["spaces"] = [ds.name for ds in datasets]
    dataset.attrs["name"] = "Memory Space Allocations"
    return dataset


def space_time_stack_highwaterconsumption_dataset(section):
    import xarray as xr

    ds = xr.Dataset(
        {
            "host_high_water_memory_consumption": (
                (),
                float(section.split()[-2]),
                {"units": "kB"},
            )
        },
        attrs={"name": "High Water Consumption"},
    )
    return ds


def kp_space_time_stack_datasets(sections):
    # fix edge case of last section
    end_section = sections[-1].pop()
    sections.append(end_section)

    datasets = []
    alloc_datasets = []
    for s, section in enumerate(sections):
        if "MAX MEMORY ALLOCATED:" in section[0]:
            name = sections[s - 1][-1][:-1]  # at end of prev. section and excludes ':'
            name = name.replace("KOKKOS ", "").replace(" SPACE", "")
            section = section[:-1]
            alloc_datasets.append(space_time_stack_allocations_dataset(name, section))
    datasets.append(combine_space_time_stack_allocations_dataset(alloc_datasets))
    datasets.append(space_time_stack_highwaterconsumption_dataset(section))

    return datasets


def convert_kp_kernel_timer_to_dataset(name, filename):
    import xarray as xr
    from pathlib import Path

    seperator = "---------------------------------------"
    sections = sections_from_lines(file_to_lines(filename), seperator)
    datasets = kp_kernel_timer_datasets(sections)
    useful_ds = xr.merge([datasets[0], datasets[2]])  # Regions and Summary
    useful_ds.attrs["name"] = name
    useful_ds.attrs["original_file"] = str(Path(filename).name)
    return useful_ds


def convert_kp_space_time_stack_to_dataset(name, filename):
    import xarray as xr
    from pathlib import Path

    seperator = "==================="
    start_line = "BEGIN KOKKOS PROFILING REPORT:\n"
    end_line = "END KOKKOS PROFILING REPORT.\n"
    lines = extract_between_lines(file_to_lines(filename), start_line, end_line)
    if lines:
        datasets = kp_space_time_stack_datasets(sections_from_lines(lines, seperator))
        useful_ds = xr.merge(
            [datasets[0], datasets[1]]
        )  # Allocations and High Water Mark
        useful_ds.attrs["name"] = name
        useful_ds.attrs["original_file"] = str(Path(filename).name)
        return useful_ds
    else:
        print(f"Warning: no KP Space Time Stack data found in {Path(filename).name}")
        return None
