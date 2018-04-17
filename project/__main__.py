import sys
import argparse

from lib import Project
from lib import Options


def run_project(args):
    options = Options()
    # options.parse(args[1:])

    parser = argparse.ArgumentParser(description='Generates leads')
    parser.add_argument('leads_number', metavar='N', type=int, nargs=1,
                        help='The number of leads to generate')
    parser.add_argument('output_file', metavar='F', type=str, nargs=1,
                        help='The output file')
    args = parser.parse_args()
    total = args.leads_number[0]

    # your script

    output_file = args.output_file[0]

    project = Project(options)

    # print 'Printing date:', project.date()
    # print 'Printing example arg:', project.print_example_arg()
    project.generate_leads(total, output_file)


if __name__ == '__main__':
    run_project(sys.argv)
