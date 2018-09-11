import time 
import RPi.GPIO as GPIO
import smbus

SM3236_ADDR         = 0x3c
SM3236_POWER        = 0x00
SM3236_PWMREG_HIGH  = 0x01      # 01H-24H,OUT1-OUT36,PWM256级
SM3236_UpdateREG    = 0x25      # 更新寄存器,01H-24H,26h-49h
SM3236_LEDConfig    = 0x26      # 26H-49H,
SM3236_RESET        = 0x4F
SM3236_ALLOFF       = 0x4A

SM3236_R            = [0x00,0x00,0xff]
SM3236_B            = [0xff,0x00,0x00]
SM3236_G            = [0x00,0xff,0x00]
SM3236_HWPWR        = 13

class SM3236(object) :
    def __init__(self,addr = 0x3c) :
        self.i2c = smbus.SMBus(1)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SM3236_HWPWR,GPIO.OUT)
        GPIO.output(SM3236_HWPWR,GPIO.LOW)

    def SM3236_PwrOn(self) :
        GPIO.output(SM3236_HWPWR,GPIO.HIGH)
        self.i2c.write_byte_data(SM3236_ADDR,SM3236_POWER,0x01)

    def SM3236_PwrOff(self) :
        self.i2c.write_byte_data(SM3236_ADDR,SM3236_POWER,0x00)
        GPIO.output(SM3236_HWPWR,GPIO.LOW)

    def SM3236_Rstreg(self) :
        self.i2c.write_byte_data(SM3236_ADDR,SM3236_RESET,0x01)

    def SM3236_Test(self,color) :
        PWM_Value = color * 12
        ON_Value = [0x01] *36
        self.i2c.write_i2c_block_data(SM3236_ADDR,SM3236_PWMREG_HIGH,PWM_Value[0:18])
        self.i2c.write_i2c_block_data(SM3236_ADDR,SM3236_PWMREG_HIGH + 0x12,PWM_Value[18:36])
        self.i2c.write_i2c_block_data(SM3236_ADDR,SM3236_LEDConfig,ON_Value[0:18])
        self.i2c.write_i2c_block_data(SM3236_ADDR,SM3236_LEDConfig + 0x12,ON_Value[18:36])
        self.i2c.write_byte_data(SM3236_ADDR,0x25,0x01)

    
def main() :
    a = SM3236()
    a.SM3236_PwrOn()
    a.SM3236_Test(SM3236_R)
    time.sleep(2)
    a.SM3236_Test(SM3236_G)
    time.sleep(2)
    a.SM3236_Test(SM3236_B)
    time.sleep(2)
    a.SM3236_Rstreg()
    a.SM3236_PwrOff()

if __name__ == '__main__' :
	main()
