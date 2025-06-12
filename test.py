import yaml
import json

def convert_yaml_to_one_line_json(yaml_file_path, json_file_path):
  """
  Converts a YAML file to a single-line JSON file.

  Args:
    yaml_file_path: The path to the input YAML file.
    json_file_path: The path to the output JSON file.
  """
  try:
    with open(yaml_file_path, 'r') as yaml_file:
      yaml_data = yaml.safe_load(yaml_file)
    
    with open(json_file_path, 'w') as json_file:
      # By removing the 'indent' parameter, the JSON is written on a single line.
      # The 'separators' argument removes whitespace after commas and colons for the most compact output.
      json.dump(yaml_data, json_file, separators=(',', ':'))
      
    print(f"Successfully converted {yaml_file_path} to a single-line JSON file: {json_file_path}")

  except FileNotFoundError:
    print(f"Error: The file {yaml_file_path} was not found.")
  except Exception as e:
    print(f"An error occurred: {e}")

# --- Example Usage ---
# Replace 'input.yaml' with the path to your YAML file
# and 'output.json' with the desired name for your JSON file.
if __name__ == "__main__":
  input_yaml = 'input.yaml'
  output_json = 'output.json'
  convert_yaml_to_one_line_json(input_yaml, output_json)
