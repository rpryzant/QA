# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree. An additional grant
# of patent rights can be found in the PATENTS file in the same directory.

import json, os, math
from collections import defaultdict

"""
Utilities for working with function program representations of questions.

Some of the metadata about what question node types are available etc are stored
in a JSON metadata file.
"""


# Handlers for answering questions. Each handler receives the scene structure
# that was output from Blender, the node, and a list of values that were output
# from each of the node's inputs; the handler should return the computed output
# value from this node.


def db_handler(scene_struct, inputs, side_inputs):
    # Just return all films in the db
    return list(range(len(scene_struct['films'])))


def make_filter_handler(attribute):
    def filter_handler(scene_struct, inputs, side_inputs):
        assert len(inputs) == 1
        assert len(side_inputs) == 1
        value = side_inputs[0]
        output = []
        for idx in inputs[0]:
            # TODO - handle missing attributes well
            atr = scene_struct['films'][idx].get(attribute, ['MISSING'])
            if value == atr or value in atr:
                output.append(idx)
        return output
    return filter_handler


def unique_handler(scene_struct, inputs, side_inputs):
    # TODO -- possibly remove this
    assert len(inputs) == 1
    if len(inputs[0]) != 1:
        return '__INVALID__'
    return inputs[0][0]


def vg_relate_handler(scene_struct, inputs, side_inputs):
    assert len(inputs) == 1
    assert len(side_inputs) == 1
    output = set()
    for rel in scene_struct['relationships']:
        if rel['predicate'] == side_inputs[0] and rel['subject_idx'] == inputs[0]:
            output.add(rel['object_idx'])
    return sorted(list(output))



def relate_handler(scene_struct, inputs, side_inputs):
    # TODO -- figure out why this is nested
    inputs = inputs[0]

    assert len(inputs) == 1
    assert len(side_inputs) == 1
    relation = side_inputs[0]

    return scene_struct['relationships'][relation][inputs[0]]
        

def union_handler(scene_struct, inputs, side_inputs):
    assert len(inputs) == 2
    assert len(side_inputs) == 0
    return sorted(list(set(inputs[0]) | set(inputs[1])))


def intersect_handler(scene_struct, inputs, side_inputs):
    assert len(inputs) == 2
    assert len(side_inputs) == 0
    return sorted(list(set(inputs[0]) & set(inputs[1])))


def count_handler(scene_struct, inputs, side_inputs):
    assert len(inputs) == 1
    return len(inputs[0])


def make_same_attr_handler(attribute):
    def same_attr_handler(scene_struct, inputs, side_inputs):
        cache_key = '_same_%s' % attribute
        if cache_key not in scene_struct:
            cache = {}
            for i, obj1 in enumerate(scene_struct['films']):
                same = []
                for j, obj2 in enumerate(scene_struct['films']):
                    if i != j and obj1[attribute] == obj2[attribute]:
                        same.append(j)
                cache[i] = same
            scene_struct[cache_key] = cache

        cache = scene_struct[cache_key]
        assert len(inputs) == 1
        assert len(side_inputs) == 0
        return cache[inputs[0]]
    return same_attr_handler


def make_query_handler(attribute):
    def query_handler(scene_struct, inputs, side_inputs):
        assert len(inputs) == 1
        assert len(side_inputs) == 0
        idx = inputs[0]
        obj = scene_struct['films'][idx]
        # assert attribute in obj
        # TODO -- handle missing values by forcing invalid. do this better?
        val = obj.get(attribute, [])
        if type(val) == list and len(val) != 1:
            return '__INVALID__'
        elif type(val) == list and len(val) == 1:
            return val[0]
        else:
            return val
    return query_handler


def exist_handler(scene_struct, inputs, side_inputs):
    assert len(inputs) == 1
    assert len(side_inputs) == 0
    return len(inputs[0]) > 0


def equal_handler(scene_struct, inputs, side_inputs):
    assert len(inputs) == 2
    assert len(side_inputs) == 0
    return inputs[0] == inputs[1]


def less_than_handler(scene_struct, inputs, side_inputs):
    assert len(inputs) == 2
    assert len(side_inputs) == 0
    return inputs[0] < inputs[1]


def greater_than_handler(scene_struct, inputs, side_inputs):
    assert len(inputs) == 2
    assert len(side_inputs) == 0
    return inputs[0] > inputs[1]


# Register all of the answering handlers here.
# TODO maybe this would be cleaner with a function decorator that takes
# care of registration? Not sure. Also what if we want to reuse the same engine
# for different sets of node types?
execute_handlers = {
    'db': db_handler,

    'filter_release_year': make_filter_handler('release_year'), 
    'filter_in_language': make_filter_handler('in_language'),
    'filter_has_imdb_votes': make_filter_handler('has_imdb_votes'),
    'filter_has_imdb_rating': make_filter_handler('has_imdb_rating'),
    'filter_has_genre': make_filter_handler('has_genre'),
    'filter_starred_actors': make_filter_handler('starred_actors'),
    'filter_written_by': make_filter_handler('written_by'),
    'filter_directed_by': make_filter_handler('directed_by'),
    'filter_title': make_filter_handler('title'),

    'unique': unique_handler,
    'relate': relate_handler,

    'union': union_handler,
    'intersect': intersect_handler,
    'count': count_handler,

    'query_release_year': make_query_handler('release_year'),  # TODO -- is this an integer or release_year? switch release_year to ints?
    'query_in_language': make_query_handler('in_language'),
    'query_has_imdb_votes': make_query_handler('has_imdb_votes'),
    'query_has_imdb_rating': make_query_handler('has_imdb_rating'),
    'query_has_genre': make_query_handler('has_genre'),
    'query_starred_actors': make_query_handler('starred_actors'),
    'query_written_by': make_query_handler('written_by'),
    'query_directed_by': make_query_handler('directed_by'),
    'query_title': make_query_handler('title'),

    'exist': exist_handler,

    # TODO -- handle list equality, etc
    'equal_integer': equal_handler,
    'equal_release_year': equal_handler,  
    'equal_in_language': equal_handler,
    'equal_has_imdb_votes': equal_handler,
    'equal_has_imdb_rating': equal_handler,
    'equal_has_genre': equal_handler,
    'equal_starred_actors': equal_handler,
    'equal_written_by': equal_handler,
    'equal_directed_by': equal_handler,
    'equal_film': equal_handler,
    'equal_title': equal_handler,

    'less_than': less_than_handler,
    'greater_than': greater_than_handler,

    'same_release_year': make_same_attr_handler('release_year'),  # TODO -- is this an integer or release_year? switch release_year to ints?
    'same_in_language': make_same_attr_handler('in_language'),
    'same_has_imdb_votes': make_same_attr_handler('has_imdb_votes'),
    'same_has_imdb_rating': make_same_attr_handler('has_imdb_rating'),
    'same_has_genre': make_same_attr_handler('has_genre'),
    'same_starred_actors': make_same_attr_handler('starred_actors'),
    'same_written_by': make_same_attr_handler('written_by'),
    'same_directed_by': make_same_attr_handler('directed_by'),
    'same_title': make_same_attr_handler('title')
}


def answer_question(question, metadata, scene_struct, all_outputs=False,
                                        cache_outputs=True):
    """
    Use structured scene information to answer a structured question. Most of the
    heavy lifting is done by the execute handlers defined above.

    We cache node outputs in the node itself; this gives a nontrivial speedup
    when we want to answer many questions that share nodes on the same scene
    (such as during question-generation DFS). This will NOT work if the same
    nodes are executed on different scenes.
    """
    all_input_types, all_output_types = [], []
    node_outputs = []
    for node in question['nodes']:
        if cache_outputs and '_output' in node:
            node_output = node['_output']
        else:
            node_type = node['type']
            msg = 'Could not find handler for "%s"' % node_type
            assert node_type in execute_handlers, msg
            handler = execute_handlers[node_type]
            node_inputs = [node_outputs[idx] for idx in node['inputs']]
            side_inputs = node.get('side_inputs', [])
            node_output = handler(scene_struct, node_inputs, side_inputs)
            if cache_outputs:
                node['_output'] = node_output
        node_outputs.append(node_output)
        if node_output == '__INVALID__':
            break

    if all_outputs:
        return node_outputs
    else:
        return node_outputs[-1]


def insert_scene_node(nodes, idx):
    # First make a shallow-ish copy of the input
    new_nodes = []
    for node in nodes:
        new_node = {
            'type': node['type'],
            'inputs': node['inputs'],
        }
        if 'side_inputs' in node:
            new_node['side_inputs'] = node['side_inputs']
        new_nodes.append(new_node)

    # Replace the specified index with a scene node
    new_nodes[idx] = {'type': 'db', 'inputs': []}

    # Search backwards from the last node to see which nodes are actually used
    output_used = [False] * len(new_nodes)
    idxs_to_check = [len(new_nodes) - 1]
    while idxs_to_check:
        cur_idx = idxs_to_check.pop()
        output_used[cur_idx] = True
        idxs_to_check.extend(new_nodes[cur_idx]['inputs'])

    # Iterate through nodes, keeping only those whose output is used;
    # at the same time build up a mapping from old idxs to new idxs
    old_idx_to_new_idx = {}
    new_nodes_trimmed = []
    for old_idx, node in enumerate(new_nodes):
        if output_used[old_idx]:
            new_idx = len(new_nodes_trimmed)
            new_nodes_trimmed.append(node)
            old_idx_to_new_idx[old_idx] = new_idx

    # Finally go through the list of trimmed nodes and change the inputs
    for node in new_nodes_trimmed:
        new_inputs = []
        for old_idx in node['inputs']:
            new_inputs.append(old_idx_to_new_idx[old_idx])
        node['inputs'] = new_inputs

    return new_nodes_trimmed


def is_degenerate(question, metadata, scene_struct, answer=None, verbose=False):
    """
    A question is degenerate if replacing any of its relate nodes with a scene
    node results in a question with the same answer.
    """
    if answer is None:
        answer = answer_question(question, metadata, scene_struct)

    for idx, node in enumerate(question['nodes']):
        if node['type'] == 'relate':
            new_question = {
                'nodes': insert_scene_node(question['nodes'], idx)
            }
            new_answer = answer_question(new_question, metadata, scene_struct)
            if verbose:
                print('here is truncated question:')
                for i, n in enumerate(new_question['nodes']):
                    name = n['type']
                    if 'side_inputs' in n:
                        name = '%s[%s]' % (name, n['side_inputs'][0])
                    print(i, name, n['_output'])
                print('new answer is: ', new_answer)

            if new_answer == answer:
                return True

    return False

