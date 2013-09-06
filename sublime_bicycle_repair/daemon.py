# -*- coding: utf-8 -*-
import os
import sys
import json
import logging
from logging import handlers
from optparse import OptionParser

# add bike too sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import bike

# remove it. WHY?
sys.path.pop(0)


def getLogger():
    """ Build file logger """
    path = '/tmp/'  # TODO
    log = logging.getLogger('')
    log.setLevel(logging.DEBUG)
    hdlr = handlers.RotatingFileHandler(
        filename=os.path.join(path, 'daemon.log'),
        maxBytes=10000000,
        backupCount=5,
        encoding='utf-8'
    )
    formatter = logging.Formatter('%(asctime)s: %(levelname)-8s: %(message)s')
    hdlr.setFormatter(formatter)
    log.addHandler(hdlr)
    return log


logger = getLogger()
bikectx = bike.init()


def write(data):
    """  Write data to STDOUT """
    if not isinstance(data, str):
        data = json.dumps(data)

    sys.stdout.write(data)

    if not data.endswith('\n'):
        sys.stdout.write('\n')

    try:
        sys.stdout.flush()
    except IOError:
        sys.exit()


class BikeFacade:
    @classmethod
    def call(cls, action, **kwargs):
        try:
            return getattr(cls, action)(**kwargs)
        except:
            logging.exception('`BikeFacade.{0}` failed'.format(action))

    @classmethod
    def rename(self, filename, line, column, new_name):
        results = []
        for match in bikectx.findReferencesByCoordinates(filename, line, column):
            if match.confidence == 100:
                results.append((match.filename, match.lineno, match.colno))

        bikectx.renameByCoordinates(filename, line, column, new_name)
        bikectx.save()
        return results

    @classmethod
    def undo(self, **kwargs):
        try:
            bikectx.undo()
        except bike.UndoStackEmptyException:
            return "UndoStackEmptyException"
        return bikectx.save()


def process_line(line):
    data = json.loads(line.strip())

    out_data = {
        'uuid': data.get('uuid'),
        'type': data['type'],
        'content': BikeFacade.call(data['type'], **data['kwargs'])
    }

    write(out_data)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option(
        "-p", "--project",
        dest="project_name",
        default='',
        help="project name to store jedi's cache"
    )
    parser.add_option(
        "-e", "--extra_folder",
        dest="extra_folders",
        default=[],
        action="append",
        help="extra folders to add to sys.path"
    )
    options, args = parser.parse_args()

    # prepare Jedi cache
    logger.info('started. extra folders - %s' % options.extra_folders)

    # append extra paths to sys.path
    for extra_folder in options.extra_folders:
        if extra_folder not in sys.path:
            sys.path.insert(0, extra_folder)

    # call the Jedi
    for line in iter(sys.stdin.readline, ''):
        if line:
            try:
                process_line(line)
            except Exception:
                logger.exception('failed to process line')
