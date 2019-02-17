import logging
import re
import sys

import cmdln

from project.lib.csv_celery_generator import CsvCeleryGenerator
from project.lib.csv_generator import CsvGenerator
from project.lib.csv_mp_generator import CsvMpGenerator
from project.lib.csv_rx_generator import CsvRxGenerator
from project.lib.utils import Utils

logging.basicConfig(format="%(name)s: %(levelname)s: %(message)s")
log = logging.getLogger("CsvRxGenerator")
RE_INT = re.compile(r'^([1-9]\d*|0)$')


class MainCommand(cmdln.Cmdln):
    name = "csv-gen"

    @cmdln.alias("rx", "mp", "se", "ce")
    @cmdln.option("-o", "--output", action="store",
                  help="the output file", dest="output")
    @cmdln.option("-r", "--rows", action="store",
                  help="number of generated rows", dest="rows")
    @cmdln.option("-b", "--bulk", action="store",
                  help="bulk size of rows written to file", dest="bulk", default='1000')
    @cmdln.option("-v", "--verbose", action="store_true",
                  help="verbose", dest="verbose")
    def do_generate_leads(self, sub_cmd, opts, *args):
        """${cmd_name}: generates leads csv data

        ${cmd_usage}
        ${cmd_option_list}
        """

        if opts.verbose:
            log.setLevel(logging.DEBUG)

        log.debug('sub_cmd: %s, opts: %s ,args %s' % (sub_cmd, opts, args))
        if opts.output is '':
            Utils.error_print('Path is missing or invalid')
            return None

        if not RE_INT.match(opts.rows):
            Utils.error_print('Number of rows is invalid')
            return None
        if not RE_INT.match(opts.bulk):
            Utils.error_print('Number of bulk is invalid')
            return None

        file_path = opts.output
        print("%s" % file_path)
        total = int(opts.rows)
        bulk = opts.bulk
        log.debug("Generating using command: %s" % sub_cmd)
        try:
            if sub_cmd == 'se':
                outfile = open(file_path, 'w+')
                log.debug("Opened file %s: " % outfile.name)
                CsvGenerator.generate_leads_file(total, outfile, int(bulk))
            if sub_cmd == 'mp':
                CsvMpGenerator.generate_leads_file(total, file_path, int(bulk))
            if sub_cmd == 'ce':
                CsvCeleryGenerator.generate_leads_file(total, int(bulk))
            if sub_cmd == 'rx':
                outfile = open(file_path, 'w+')
                log.debug("Opened file %s: " % outfile.name)
                CsvRxGenerator.generate_leads_file(total, outfile, int(bulk))
        except (OSError, IOError):
            Utils.error_print('Path is invalid: %s' % file_path)
            log.error("Failed to open file {}:".format(file_path))
            return None


def main():
    command = MainCommand()
    sys.exit(command.main())


if __name__ == "__main__":
    main()
