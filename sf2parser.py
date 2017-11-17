from struct import unpack
from sf2utils.generator import Sf2Gen
from sf2lib.sf2file import *
from sf2lib.sf2tags import SF2Tags


class SF2Parser:

    def __init__(self, file):

        self.file = file
        self.riff = unpack('<4sL4s', self.file.read(12))
        self.data = list(self.read_next_tag())
        self.size = self.data[0][1]
        self.tagged_data = self.get_dict()
        self.file.close()

        self.INFO = self.get_info()
        self.sdta = self.get_sdta()
        self.pdta = self.get_pdta()

        self.sf2file = SF2File(info=self.INFO, sdta=self.sdta, pdta=self.pdta)

    def read_next_tag(self):
        while self.file.tell() < self.riff[1]:
            tag = self.file.read(4)
            if tag in SF2Tags.riff_tags:
                chunk = tag, 0
            else:
                length = unpack('<L', self.file.read(4))[0]
                if tag == b'LIST':
                    chunk = tag, length
                else:
                    chunk = tag, (length, self.file.read(length))
            yield chunk

    def parse_fixed_chunk(self, size, struct_type, tag):
        data_length = self.tagged_data[tag][0]
        blocks = []
        binary_data = self.tagged_data[tag][1]
        nblocks = data_length//size     # get the number of blocks in chunk
        for cnt in range(nblocks):
            offset = size * cnt
            data = unpack(struct_type, binary_data[offset:offset + size])
            blocks.append(data)
        return blocks

    def get_dict(self):
        d = dict(filter(lambda x: x[0] != b'LIST', self.data))
        return d

    def get_info(self):
        data = {}
        for (tag, value) in self.data:
            if tag in SF2Tags.INFO:
                if tag == b'ifil' or tag == b'iver':
                    data[tag.decode()] = self.parse_fixed_chunk(4, '<HH', tag)[0]
                else:
                    data[tag.decode().lower()] = self.tagged_data[tag][1].decode('latin-1')
        return SF2INFO(**data)

    def get_sdta(self):
        data = dict()
        data['smpl'] = self.tagged_data.get(b'smpl')
        data['sm24'] = self.tagged_data.get(b'sm24')
        # skip 4 bytes of chunk length
        if data['smpl']:
            data['smpl'] = data['smpl'][1]
        if data['sm24']:
            data['sm24'] = data['sm24'][1]
        return SF2sdta(**data)

    def get_pdta(self):
        data = {}
        for tag in self.tagged_data:
            if tag in SF2Tags.pdta:
                data[tag.decode()] = self.parse_fixed_chunk(*SF2Tags.pdta[tag], tag)
        return SF2pdta(**data)

# TODO constraints, exceptions
# TODO class Preset, generator, Bag, Instruments


if __name__ == '__main__':
    file = open('Florestan_String_Quartet.sf2', 'rb')







