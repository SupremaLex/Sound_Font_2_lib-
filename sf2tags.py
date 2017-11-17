class SF2Tags:

    riff_tags = [b'RIFF', b'sfbk', b'INFO', b'sdta', b'pdta']

    INFO = [b'ifil', b'isng', b'INAM', b'irom', b'iver', b'ICRD', b'IENG',
            b'IPRD', b'ICOP', b'ICMT', b'ISFT']

    sdta = [b'smpl', b'sm24']

    pdta = {b'phdr': (38, '<20s3H3L'), b'pbag': (4, '<HH'), b'pmod': (10, '<5H'),
                            b'pgen': (4, '<HH'), b'inst': (22, '<20sH'), b'ibag': (4, '<HH'),
                            b'imod': (10, '<5H'), b'igen': (4, '<HH'), b'shdr': (46, '<20s5LBbHH')
            }

    tags = riff_tags + INFO + sdta + list(pdta.keys())




