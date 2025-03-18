import json
import argparse
import os

def gc_to_swfastedit_format(gc_dict):
    swfast_dict = {
        "tumor": [],
        "background": []
    }
    for point in gc_dict.get("points", []):
        if point["name"] == "tumor":
            swfast_dict["tumor"].append(point["point"])
        elif point["name"] == "background":
            swfast_dict["background"].append(point["point"])
    return swfast_dict

def swfast_to_gc_format(swfast_json_path, gc_json_path):
    assert os.path.exists(swfast_json_path)
    
    with open(swfast_json_path, 'r') as f:
        json_data = json.load(f)
        fg_points = json_data.get('tumor', [])
        bg_points = json_data.get('background', [])
        gc_dict = {  
            "version": {"major": 1, "minor": 0},  
            "type": "Multiple points",  
            "points": []
        }
        for fg_point in fg_points:
            gc_dict['points'].append({'point': fg_point, 'name': 'tumor'})
        for bg_point in bg_points:
            gc_dict['points'].append({'point': bg_point, 'name': 'background'})
        with open(gc_json_path, 'w') as f_gc:
            json.dump(gc_dict, f_gc)
    print(f'Finished converting {swfast_json_path} to {gc_json_path} in the GC format!')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert SWFast format to GC format')
    parser.add_argument('--swfast_json_path', type=str, help='Path to the SWFast JSON file')
    parser.add_argument('--gc_json_path', type=str, help='Path to the output GC JSON file')
    args = parser.parse_args()
    swfast_to_gc_format(args.swfast_json_path, args.gc_json_path)