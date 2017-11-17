

class SF2Sample:

    DEFAULT_PITCH = 60
    UNPITCHED_PITCH = 255
    INVALID_LOW_PITCH = 128
    INVALID_HIGH_PITCH = 254

    CHANNEL_MONO = 1
    CHANNEL_RIGHT = 2
    CHANNEL_LEFT = 4
    CHANNEL_MASK = 0x07

    def __init__(self, sdta, **params):
        self.name = params.get('name').decode('latin1')
        if self.name == 'EOS':
            return
        self.start = params.get('start')
        self.end = params.get('end')
        self.start_loop = params.get('start_loop')
        self.end_loop = params.get('end_loop')
        self.rate = params.get('rate')
        self.pitch = params.get('pitch')
        self.correction_pitch = params.get('correction')
        self.sample_link = params.get('smplink')
        self.sample_type = params.get('type')

        self.smpl_data = sdta.smpl
        self.sm24_data = sdta.sm24

    @property
    def is_mono(self):
        return self.sample_type & SF2Sample.CHANNEL_MONO

    @property
    def is_left(self):
        return self.sample_type & SF2Sample.CHANNEL_LEFT

    @property
    def duration(self):
        return self.end - self.start

    @property
    def loop_duration(self):
        return self.end_loop - self.start_loop

    @property
    def get_sample_data(self):
        if self.smpl_data:
            # get top 16 bits
            sample_16 = self.smpl_data[self.start*2: self.start*2+self.duration*2]
        else:
            raise ValueError("WTF")
        if self.sm24_data:
            # get lower 8 bits
            sample_8 = self.sm24_data[self.start: self.start + self.duration]
        else:
            return sample_16

        # merge 16 and 8 bits
        result = []
        for ind in range(self.duration):
            result.extend(sample_16[ind: ind+2])
            result.append(sample_8[ind])
        return bytearray(result)

    def __str__(self):
        if self.name == 'EOS':
            return 'EOS'
        result = "Sample {0.name} from {0.start} to {0.end}, loop from {0.start_loop} to {0.end_loop}, "\
                 "frequency {0.rate}Hz "

        if self.correction_pitch:
            result += "replay correction {0.correction_pitch} cent(s) "

        if self.pitch != SF2Sample.DEFAULT_PITCH:
            result += "original pitch {0.pitch} "

        if self.is_mono:
            result += "MONO"
        else:
            if self.is_left:
                result += "LEFT"
            else:
                result += "RIGHT"

            if self.sample_link:
                result += " linked to sample {0.sample_link}"
        return result.format(self)

# TODO export method and constraints, exceptions

