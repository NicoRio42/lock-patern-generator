# Lock pattern generator

## Introduction

This is a Python script to generate "Android like" lock patterns in svg format. The image bellow is an exemple of the svg files that can be generated.

![Exemple lock pattern generated with the script](./exemple_lock_pattern.svg)

I writed this script because I needed 120 of these lock patterns for an [orienteering](https://en.wikipedia.org/wiki/Orienteering) project. I was in charge of printing the checkpoints with such lock patterns on each of them.

The script is made to generate nice looking lock patterns:
- A segment between two nodes doesn't appear twice in a pattern.
- Angles between segments at nodes are higher than 45 degrees.

## Settup

Clone the repository.

Create and activate a virtual environment.

```
python -m virtualenv env
./env/scripts/activate.ps1
```

install packages in requirements.txt

```
pip install requirements.txt
```

## Usage

Exemple:

```
python lock_pattern_generator.py --pattern_number 10 --min_node 2 --max_node 6
```

Options:

| Option           | Description                          | Default |
|------------------|--------------------------------------|---------|
| --pattern_number | Number of patterns to generate       | 5       |
| --min_node       | Minimum number of connected nodes    | 2       |
| --max_node       | Maximum number of connected nodes    | 5       |

The svg files are generated in the \out folder. An index Excel file is also generated.