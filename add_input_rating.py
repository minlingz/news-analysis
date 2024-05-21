import json
import argparse


def read_json(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def write_json(data, file_path):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


def add_ratings(json_data):
    for item in json_data:
        print(f"Body: \n {item.get('body', 'N/A')}")
        print(f"Distinctive Events: \n {item.get('distinctive_events', 'N/A')}")
        rating = input("Enter rating for this item: ")
        item["rating"] = rating
    return json_data


def main():
    parser = argparse.ArgumentParser(description="Add ratings to items in a JSON file.")
    parser.add_argument("input_file", help="Path to the input JSON file")

    args = parser.parse_args()

    input_file = args.input_file
    output_file = "rating_" + input_file  # Path to your output JSON file

    # Read the JSON file
    data = read_json(input_file)

    # Add ratings to each item
    data_with_ratings = add_ratings(data)

    # Save the modified JSON data to a new file
    write_json(data_with_ratings, output_file)
    print(f"Modified JSON data has been saved to {output_file}")


if __name__ == "__main__":
    main()
