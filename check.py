import json
import re

def diagnose_json(content):
    try:
        json.loads(content)
        return True, content
    except json.JSONDecodeError as e:
        return False, str(e)

def fix_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Attempt to load the JSON to see if it is already valid
        is_valid, result = diagnose_json(content)
        if is_valid:
            print("The JSON file is already valid.")
            return json.loads(content)
        else:
            print(f"Initial JSON is invalid: {result}")
            print("Attempting to fix common issues...")

        # Fix common issues
        fixed_content = content.replace("\'", "\"")  # Replace single quotes with double quotes
        fixed_content = re.sub(r',\s*}', '}', fixed_content)  # Remove trailing commas before closing brace
        fixed_content = re.sub(r',\s*]', ']', fixed_content)  # Remove trailing commas before closing bracket

        is_valid, result = diagnose_json(fixed_content)
        if is_valid:
            print("JSON file has been fixed with common issue fixes.")
            json_data = json.loads(fixed_content)
        else:
            print(f"Still unable to fix JSON file: {result}")
            print("Attempting line-by-line fix...")

            lines = content.splitlines()
            fixed_lines = []
            errors = []

            for idx, line in enumerate(lines, start=1):
                fixed_line = line.replace("\'", "\"")
                fixed_line = re.sub(r',\s*}', '}', fixed_line)
                fixed_line = re.sub(r',\s*]', ']', fixed_line)
                
                is_valid, result = diagnose_json(fixed_line)
                if not is_valid:
                    errors.append((idx, line, result))
                    print(f"Line {idx}: {result}")
                    print(f"Content: {line}")
                else:
                    fixed_lines.append(fixed_line)

            if errors:
                print("Some lines could not be fixed automatically. Please review the following issues:")
                for error in errors:
                    print(f"Line {error[0]}: {error[2]}")
                    print(f"Content: {error[1]}")
                return None

            fixed_content = "\n".join(fixed_lines)

            is_valid, result = diagnose_json(fixed_content)
            if is_valid:
                print("JSON file has been fixed with line-by-line fixes.")
                json_data = json.loads(fixed_content)
            else:
                print(f"Line-by-line fix failed: {result}")
                return None

        # Save the fixed JSON
        fixed_file_path = file_path.replace('.json', '_fixed.json')
        with open(fixed_file_path, 'w', encoding='utf-8') as fixed_file:
            json.dump(json_data, fixed_file, indent=4)

        print(f"Fixed JSON file saved as: {fixed_file_path}")
        return json_data

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except UnicodeDecodeError as e:
        print(f"Failed to read the file due to encoding error: {e}")
        return None

# Example usage:
file_path = 'scraped.json'
fixed_data = fix_json(file_path)
