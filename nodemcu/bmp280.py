# Save this file in nodemcu with bmp280.py name
import time
import struct

class BMP280:
    def __init__(self, i2c, addr=0x76):
        self.i2c = i2c
        self.addr = addr
        if self.addr not in i2c.scan():
            raise OSError("BMP280 not found at I2C address {}".format(addr))

        self._load_calibration()
        self._write_reg(0xF4, 0x27)
        self._write_reg(0xF5, 0xA0)

    def _read_reg(self, reg, nbytes=1):
        return self.i2c.readfrom_mem(self.addr, reg, nbytes)

    def _write_reg(self, reg, value):
        self.i2c.writeto_mem(self.addr, reg, bytes([value]))

    def _load_calibration(self):
        calib = self._read_reg(0x88, 24)
        self.dig_T1, self.dig_T2, self.dig_T3 = struct.unpack('<Hhh', calib[:6])
        self.dig_P1, self.dig_P2, self.dig_P3, self.dig_P4, self.dig_P5, \
        self.dig_P6, self.dig_P7, self.dig_P8, self.dig_P9 = struct.unpack('<Hhhhhhhhh', calib[6:])
        self.t_fine = 0

    def _read_raw_data(self):
        data = self._read_reg(0xF7, 6)
        adc_p = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        adc_t = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        return adc_t, adc_p

    @property
    def temperature(self):
        adc_t, _ = self._read_raw_data()
        var1 = ((((adc_t >> 3) - (self.dig_T1 << 1))) * self.dig_T2) >> 11
        var2 = (((((adc_t >> 4) - self.dig_T1) * ((adc_t >> 4) - self.dig_T1)) >> 12) * self.dig_T3) >> 14
        self.t_fine = var1 + var2
        T = (self.t_fine * 5 + 128) >> 8
        return T / 100

    @property
    def pressure(self):
        _, adc_p = self._read_raw_data()
        var1 = self.t_fine - 128000
        var2 = var1 * var1 * self.dig_P6
        var2 = var2 + ((var1 * self.dig_P5) << 17)
        var2 = var2 + (self.dig_P4 << 35)
        var1 = ((var1 * var1 * self.dig_P3) >> 8) + ((var1 * self.dig_P2) << 12)
        var1 = (((1 << 47) + var1) * self.dig_P1) >> 33
        if var1 == 0:
            return 0
        p = 1048576 - adc_p
        p = (((p << 31) - var2) * 3125) // var1
        var1 = (self.dig_P9 * (p >> 13) * (p >> 13)) >> 25
        var2 = (self.dig_P8 * p) >> 19
        p = ((p + var1 + var2) >> 8) + (self.dig_P7 << 4)
        return p / 25600
