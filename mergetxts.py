import os

def merge_text_files(start_index, end_index, output_file):
    with open(output_file, 'w') as outfile:
        for i in range(start_index, end_index + 1):
            filename = f"extracted_text_{i}.txt"
            if os.path.exists(filename):
                with open(filename, 'r') as infile:
                    outfile.write(infile.read() + "\n\n")
                print(f"Added {filename} to {output_file}")
            else:
                print(f"Warning: {filename} does not exist and was skipped.")

def main():
    output_filename = 'merged_text_files.txt'
    merge_text_files(1, 67, output_filename)
    print(f"All text files have been merged into {output_filename}")

if __name__ == "__main__":
    main()
