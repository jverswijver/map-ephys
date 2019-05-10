# map-ephys interative shell module

import os
import sys
import logging
import warnings
from code import interact

import datajoint as dj

from pipeline import ephys
from pipeline import lab
from pipeline import experiment
from pipeline import ccf
from pipeline import tracking
from pipeline import psth
from pipeline import publication


log = logging.getLogger(__name__)


def usage_exit():
    print("usage: {p} [{c}]"
          .format(p=os.path.basename(sys.argv[0]),
                  c='|'.join(list(actions.keys()))))
    sys.exit(0)


def logsetup(*args):
    logging.basicConfig(level=logging.ERROR)
    log.setLevel(logging.DEBUG)
    logging.getLogger('pipeline.ingest.behavior').setLevel(logging.DEBUG)
    logging.getLogger('pipeline.ingest.ephys').setLevel(logging.DEBUG)
    logging.getLogger('pipeline.ingest.tracking').setLevel(logging.DEBUG)
    logging.getLogger('pipeline.ingest.histology').setLevel(logging.DEBUG)
    logging.getLogger('pipeline.psth').setLevel(logging.DEBUG)
    logging.getLogger('pipeline.ccf').setLevel(logging.DEBUG)
    logging.getLogger('pipeline.publication').setLevel(logging.DEBUG)


def ingest_behavior(*args):
    from pipeline.ingest import behavior as ingest_behavior
    ingest_behavior.BehaviorIngest().populate(display_progress=True)


def ingest_ephys(*args):
    from pipeline.ingest import ephys as ingest_ephys
    ingest_ephys.EphysIngest().populate(display_progress=True)


def ingest_tracking(*args):
    from pipeline.ingest import tracking as ingest_tracking
    ingest_tracking.TrackingIngest().populate(display_progress=True)


def ingest_histology(*args):
    from pipeline.ingest import histology as ingest_histology
    ingest_histology.HistologyIngest().populate(display_progress=True)


def populate_psth(*args):
    log.info('psth.Condition.populate()')
    psth.Condition.populate()

    log.info('psth.CellPsth.populate()')
    psth.CellPsth.populate()

    log.info('psth.Selectivity.populate()')
    psth.Selectivity.populate()

    log.info('psth.CellGroupCondition.populate()')
    psth.CellGroupCondition.populate()

    log.info('psth.CellGroupPsth.populate()')
    psth.CellGroupPsth.populate()


def publish(*args):
    publication.ArchivedRawEphysTrial.populate()


def shell(*args):
    modules = [lab, experiment, ephys, tracking, ccf, psth, publication]
    interact('map shell.\n\nschema modules:\n\n  - {m}\n'
             .format(m='\n  - '.join(
                 '.'.join(m.__name__.split('.')[1:]) for m in modules)),
             local=globals())


def ccfload(*args):
    ccf.CCFAnnotation.load_ccf_r3_20um()


def erd(*args):
    for mod in (ephys, lab, experiment, tracking, psth, ccf, publication):
        modname = str().join(mod.__name__.split('.')[1:])
        fname = os.path.join('pipeline', '{}.png'.format(modname))
        print('saving', fname)
        dj.ERD(mod, context={modname: mod}).save(fname)


actions = {
    'ingest-behavior': ingest_behavior,
    'ingest-ephys': ingest_ephys,
    'ingest-tracking': ingest_tracking,
    'ingest-histology': ingest_histology,
    'populate-psth': populate_psth,
    'publish': publish,
    'shell': shell,
    'erd': erd,
    'ccfload': ccfload,
}