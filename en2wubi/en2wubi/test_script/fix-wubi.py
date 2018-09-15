import sys
import os
import en2wubi as e2w
if __name__ == '__main__':
    input_file_name = sys.argv[1]
    input_file_name = os.path.join(
        e2w.E2W_DATA_PATH, input_file_name)
    output_file_path = "{}.fix".format(input_file_name)
    try:
        output_file = open(output_file_path, "w")
    except:
        output_file = open(output_file_path, "wb")
    for line in open(input_file_name):
        line = line.strip()
        line = line.replace("  ", "@")
        line = line.replace(" ", "|")
        line = line.replace("@", " ")
        for punct in ".,();#<>/\\":
            line = line.replace("|{}".format(punct), " {}".format(punct))
            line = line.replace("{}|".format(punct), "{} ".format(punct))
        line = "{}\n".format(line)
        line.replace("|\n", "\n")
        output_file.write(line)
    output_file.close()
