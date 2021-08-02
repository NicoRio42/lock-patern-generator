import os
from xml.dom.minidom import parse
import random
import math

import click
from openpyxl import Workbook

def angle_between_segments(nodes):
    """Return the angle formed by 3 consecutives nodes of the pattern
    in degrees"""
    coord = []
    for node in nodes:
        if node in [1, 4, 7]:
            x = 0
        if node in [2, 5, 8]:
            x = 1
        if node in [3, 6, 9]:
            x = 2
        if node in [1, 2, 3]:
            y = 0
        if node in [4, 5, 6]:
            y = 1
        if node in [7, 8, 9]:
            y = 2
        coord.append([x, y])
    
    angle = math.atan2(coord[2][1] - coord[1][1], coord[2][0] - \
        coord[1][0]) - math.atan2(coord[0][1] - coord[1][1], coord[0][0] - \
        coord[1][0])
    return abs(math.degrees(angle))

def generate_node(pattern):
    last_node = pattern[-1]
    nodes_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    # no consecutive equal nodes
    nodes_list.remove(last_node)

    # Line should not cross another node
    if last_node != 5:
        nodes_list.remove(10 - last_node)
    if last_node == 1:
        nodes_list = [j for j in nodes_list if (j not in [3, 7])]
    if last_node == 3:
        nodes_list = [j for j in nodes_list if (j not in [1, 9])]
    if last_node == 7:
        nodes_list = [j for j in nodes_list if (j not in [1, 9])]
    if last_node == 9:
        nodes_list = [j for j in nodes_list if (j not in [3, 7])]

    if len(pattern) > 1:
        for i in range(len(pattern) - 1):
            if pattern[i] == last_node:
                # Not twice the same path
                nodes_list = [j for j in nodes_list if j != pattern[i + 1]]
            
            if pattern[i + 1] == last_node:
                # Not twice the same reverse path
                nodes_list = [j for j in nodes_list if j != pattern[i]]
    
        # No angles lower than 45 degrees
        nodes_list = [j for j in nodes_list if \
            angle_between_segments([pattern[-2], pattern[-1], j]) > 45]
    
    # Return None if the is no possible node
    if nodes_list:
        return random.choice(nodes_list)
    else:
        return None

def generate_svg(template, pattern, id):
    """Create a svg file in the out directory for the lock pattern"""

    rootNode = template.documentElement
    polyline = rootNode.getElementsByTagName('polyline')[0]
    
    coord_list = []
    for node in pattern:
        if node in [1, 4, 7]:
            x = 11
        if node in [2, 5, 8]:
            x = 32
        if node in [3, 6, 9]:
            x = 53
        if node in [1, 2, 3]:
            y = 11
        if node in [4, 5, 6]:
            y = 32
        if node in [7, 8, 9]:
            y = 53
        coord_list.append(str(x) + ',' + str(y))
    
    points = ' '.join(coord_list)

    polyline.setAttribute('points', points)

    # Create "out" directory if it don't already exists
    if not os.path.exists(r".\out"):
        os.mkdir(r".\out")

    string_pattern = [str(i) for i in pattern]
    filename = os.path.join(
        'out',
        str(id) + '_' + ''.join(string_pattern) + '.svg'
    )

    with open(filename, 'w') as f:
	    template.writexml(f, addindent='  ', encoding='utf-8')

@click.command()
@click.option(
    '--pattern_number',
    prompt='Number of patterns to generate',
    default=1,
    help='Number of patterns to generate.'
)
@click.option(
    '--min_node',
    prompt='Minimum number of connected nodes',
    default=2,
    help='Minimum number of connected nodes.'
)
@click.option(
    '--max_node',
    prompt='Maximum number of connected nodes',
    default=5,
    help='Maximum number of connected nodes.'
)
def generator(pattern_number, min_node, max_node):
    """Generate random "Android like" lock patterns in svg format."""

    template = parse("lock_pattern_template.svg")
    patterns = []

    for i in range(pattern_number):
        while True:
            nodes_number = random.randint(min_node, max_node)
            pattern = [random.randint(1, 9)] # random first node

            for j in range(1, nodes_number):
                node = generate_node(pattern)
                # Break the loop if there is no possible node
                if node:
                    pattern.append(node)
                else:
                    break
            
            # Not twice the same pattern
            if pattern not in patterns or reversed(pattern) not in patterns:
                break
        
        patterns.append(pattern)

    id = 1

    # Index excel file initialisation
    wb = Workbook()
    ws1 = wb.active
    ws1.append(['Id', 'Pattern'])

    for pattern in patterns:
        generate_svg(template, pattern, id)
        # Adding line to Excel file
        ws1.append([id, int(''.join([str(i) for i in pattern]))])
        id += 1
    
    xlsx_filename = os.path.join('out', 'index.xlsx')
    # Create "out" directory if it don't already exists
    if not os.path.exists(r".\out"):
        os.mkdir(r".\out")
    wb.save(filename = xlsx_filename)

if __name__ == '__main__':
    generator()