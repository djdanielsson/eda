# https://stackoverflow.com/questions/13319067/parsing-yaml-return-with-line-number
from yaml.composer import Composer
from yaml.constructor import Constructor
from yaml.nodes import ScalarNode
from yaml.resolver import BaseResolver
from yaml.loader import Loader
from pprint import pprint
import subprocess
import os

DEBUG = True

class LineLoader(Loader):
  def __init__(self, stream):
    super(LineLoader, self).__init__(stream)

  def compose_node(self, parent, index):
    # the line number where the previous token has ended (plus empty lines)
    line = self.line
    node = Composer.compose_node(self, parent, index)
    node.__line__ = line + 1
    return node

  def construct_mapping(self, node, deep=False):
    node_pair_lst = node.value
    node_pair_lst_for_appending = []

    for key_node, value_node in node_pair_lst:
      shadow_key_node = ScalarNode(tag=BaseResolver.DEFAULT_SCALAR_TAG, value='__line__' + key_node.value)
      shadow_value_node = ScalarNode(tag=BaseResolver.DEFAULT_SCALAR_TAG, value=key_node.__line__)
      node_pair_lst_for_appending.append((shadow_key_node, shadow_value_node))

    node.value = node_pair_lst + node_pair_lst_for_appending
    mapping = Constructor.construct_mapping(self, node, deep=deep)
    return mapping

if __name__ == '__main__':
  #files = os.system("git diff --unified=0 --diff-filter=M HEAD~1 HEAD | grep -v -e '^[+-]' -e '^index' | sed 's/diff --git a.* b\//\//g; s/.*@@\(.*\)@@.*/\1/g; s/^ -//g; s/,[0-9]*//g; s/\(^[0-9]*\) +/\1-/g;'")
  #['git', 'diff', '--unified=0', '--diff-filter=M', 'HEAD~1', 'HEAD', '|', 'grep', '-v', '-e', '^[+-]', '-e', '^index', '|', 'sed', 's/diff --git a.* b\//\//g; s/.*@@\(.*\)@@.*/\1/g; s/^ -//g; s/,[0-9]*//g; s/\(^[0-9]*\) +/\1-/g;']
  #files = (((subprocess.run(['git', 'diff', '--diff-filter=M', 'HEAD~5', 'HEAD', '--name-only'], stdout=subprocess.PIPE)).stdout).decode()).split('\n')
  #files = (((subprocess.run(['git', 'diff', '--unified=0', '--diff-filter=M', 'HEAD~1', 'HEAD', '|', 'grep', '-v', '-e', '^[+-]', '-e', '^index', '|', 'sed', 's/diff --git a.* b\//\//g; s/.*@@\(.*\)@@.*/\1/g; s/^ -//g; s/,[0-9]*//g; s/\(^[0-9]*\) +/\1-/g;'], shell=True, stdout=subprocess.PIPE)).stdout).decode()).split('\n')
  files = (((subprocess.run(["git diff --unified=0 --diff-filter=M HEAD~1 HEAD | grep -v -e '^[+-]' -e '^index' | sed 's/diff --git a.* b\//\//g; s/.*@@\(.*\)@@.*/\1/g; s/^ -//g; s/,[0-9]*//g; s/\(^[0-9]*\) +/\1-/g;'"], shell=True, stdout=subprocess.PIPE)).stdout).decode()).split('\n')
  print(files) if DEBUG else None
  for each in files:
    print(each) if DEBUG else None
    if ".yml" in each:
      print(each) if DEBUG else None
      print("IF") if DEBUG else None
      current_path = os.getcwd()
      print(current_path) if DEBUG else None
      path = current_path + each
      print(path) if DEBUG else None
      loader = LineLoader(open(path).read())
      data = loader.get_single_data()

      pprint(data)
