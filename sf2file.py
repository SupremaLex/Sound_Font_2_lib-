from sf2lib.sf2sample import SF2Sample
from sf2lib.sf2instrument import SF2Instrument
from sf2lib.sf2preset import SF2Preset
from collections import namedtuple


class SF2File:

    Phdr = namedtuple('Phdr', ['name', 'number', 'bank', 'bag', 'library', 'genre', 'morphology'])
    Pbag = namedtuple('Pbag', ['generator', 'modulator'])
    Pmod = namedtuple('Pmod', ['src', 'dst', 'amount', 'amtsrc', 'trans'])
    Pgen = namedtuple('Pgen', ['oper', 'amount'])
    Inst = namedtuple('Inst', ['name', 'bag'])
    Ibag = namedtuple('Ibag', ['generator', 'modulator'])
    Imod = namedtuple('Imod', ['src', 'dst', 'amount', 'amtsrc', 'trans'])
    Igen = namedtuple('Igen', ['type', 'amount'])
    Shdr = namedtuple('Shdr', ['name', 'start', 'end', 'start_loop', 'end_loop', 'rate', 'pitch',
                               'correction', 'smplink', 'type'])

    def __init__(self, *, info, sdta, pdta):
        self.INFO = info
        self.sdta = sdta
        self.pdta = pdta

    @property
    def samples(self):
        samples = [SF2Sample(sdta=self.sdta, **sm._asdict()) for sm in self.pdta.shdr]
        return samples

    @property
    def instruments(self):
        instruments = [SF2Instrument(**ins._asdict()) for ins in self.pdta.inst]
        return instruments

    @property
    def presets(self):
        presets = [SF2Preset(**pr._asdict()) for pr in self.pdta.phdr]
        return presets


class SF2INFO:

    def __init__(self, **tags):
        self.ifil = tags.get('ifil')
        self.isng = tags.get('isng')
        self.INAM = tags.get('inam')
        self.irom = tags.get('irom')
        self.iver = tags.get('iver')
        self.ICRD = tags.get('icrd')
        self.IENG = tags.get('ieng')
        self.IPRD = tags.get('iprd')
        self.ICOP = tags.get('icop')
        self.ICMT = tags.get('icmt')
        self.ISFT = tags.get('isft')

    def __str__(self):
        result = """Version: {0.ifil[0]}.{0.ifil[1]}
                    \rSound engine: {0.isng}
                    \rSoundFont bank: {0.INAM}
                    \rROM: {0.irom}
                    \rROM version: {0.iver}
                    \rCreation date: {0.ICRD}
                    \rSound designers or engineers: {0.IENG}
                    \rIntended product: {0.IPRD}
                    \rCopyright: {0.ICOP}
                    \rComments: {0.ICMT}
                    \rCompatible tools: {0.ISFT}""".format(self)
        return result


class SF2sdta:

    def __init__(self, **tags):
        self.smpl = tags.get('smpl')
        self.sm24 = tags.get('sm24')


class SF2pdta:

    def __init__(self, **tags):
        self._phdr = tags.get('phdr')
        self._pbag = tags.get('pbag')
        self._pmod = tags.get('pmod')
        self._pgen = tags.get('pgen')
        self._inst = tags.get('inst')
        self._ibag = tags.get('ibag')
        self._imod = tags.get('imod')
        self._igen = tags.get('igen')
        self._shdr = tags.get('shdr')

    @property
    def phdr(self):
        data = [SF2File.Phdr(*e) for e in self._phdr]
        return data

    @property
    def pbag(self):
        data = [SF2File.Pbag(*e) for e in self._pbag]
        return data

    @property
    def pmod(self):
        data = [SF2File.Pmod(*e) for e in self._pmod]
        return data

    @property
    def pgen(self):
        data = [SF2File.Pgen(*e) for e in self._pgen]
        return data

    @property
    def inst(self):
        data = [SF2File.Shdr(*e) for e in self._inst]
        return data

    @property
    def ibag(self):
        data = [SF2File.Pbag(*e) for e in self._ibag]
        return data

    @property
    def imod(self):
        data = [SF2File.Pmod(*e) for e in self._imod]
        return data

    @property
    def igen(self):
        data = [SF2File.Pgen(*e) for e in self._igen]
        return data

    @property
    def shdr(self):
        data = [SF2File.Shdr(*e) for e in self._shdr]
        return data

# TODO constraints, exceptions


