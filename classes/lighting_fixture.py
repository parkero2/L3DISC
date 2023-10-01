from stupidArtnet import StupidArtnet

class LightingFixture:
    def __init__(self, ArtnetController: StupidArtnet, headID: int, 
                 headType: str, channels:int, patch: int, intensity: int=None, 
                 red:int=None, green:int=None, blue:int=None, amber:int=None, 
                 white:int=None, pan:int=None, tilt:int=None):
        # Channels and general DMX stuff
        self.ArtnetController = ArtnetController
        self.headID = headID
        self.headType = headType
        self.channels = channels
        self.patch = patch
        self.intensity = intensity
        self.red = red
        self.green = green
        self.blue = blue
        self.amber = amber
        self.white = white
        self.pan = pan
        self.tilt = tilt

        # Values of the channels
        self.intensityValue = None
        self.redValue = None
        self.greenValue = None
        self.blueValue = None
        self.amberValue = None
        self.whiteValue = None
        self.panValue = None
        self.tiltValue = None

        # Other stuff for programming
        self.allChans = [self.intensity + self.patch, self.red + self.patch, 
                         self.green + self.patch, self.blue + self.patch, 
                         self.amber + self.patch, self.white + self.patch, 
                         self.pan + self.patch, self.tilt + self.patch]
        self.isActive = False
        
    def get_all_channels(self) -> list:
        return self.allChans
    
    def blackMeOut(self):
        self.set_intensity(0)
        self.set_red(0)
        self.set_green(0)
        self.set_blue(0)
        self.set_amber(0)
        self.set_white(0)
        self.set_pan(0)
        self.set_tilt(0)
        self.isActive = False


    def get_intensity(self) -> int:
        return self.intensity
    
    def set_intensity(self, intensity: int):
        self.isActive = True
        self.intensityValue = intensity
        self.ArtnetController.set_single_value(self.patch + self.intensity, 
                                               self.intensityValue)
    
    def get_red(self) -> int:
        return self.redValue
    
    def set_red(self, red: int):
        self.isActive = True
        self.redValue = red
        self.ArtnetController.set_single_value(self.patch + self.red, 
                                               self.redValue)

    def get_green(self) -> int:
        return self.greenValue

    def set_green(self, green: int):
        self.isActive = True
        self.greenValue = green
        self.ArtnetController.set_single_value(self.patch + self.green, 
                                               self.greenValue)
        
    def get_blue(self) -> int:
        return self.blueValue
    
    def set_blue(self, blue: int):
        self.isActive = True
        self.blueValue = blue
        self.ArtnetController.set_single_value(self.patch + self.blue, 
                                               self.blueValue)
        
    def get_amber(self) -> int:
        return self.amberValue
    
    def set_amber(self, amber: int):
        self.isActive = True
        self.amberValue = amber
        self.ArtnetController.set_single_value(self.patch + self.amber, 
                                               self.amberValue)
        
    def get_white(self) -> int:
        return self.whiteValue
    
    def set_white(self, white: int):
        self.isActive = True
        self.whiteValue = white
        self.ArtnetController.set_single_value(self.patch + self.white, 
                                               self.whiteValue)
        
    def get_pan(self) -> int:
        return self.panValue
    
    def set_pan(self, pan: int):
        self.isActive = True
        self.panValue = pan
        self.ArtnetController.set_single_value(self.patch + self.pan, 
                                               self.panValue)
        
    def get_tilt(self) -> int:
        return self.tiltValue
    
    def set_tilt(self, tilt: int):
        self.isActive = True
        self.tiltValue = tilt
        self.ArtnetController.set_single_value(self.patch + self.tilt, 
                                               self.tiltValue)
    
    def get_isActive(self) -> bool:
        return self.isActive
    
    def get_headType(self) -> str:
        return self.headType
    
    def get_headID(self) -> int:
        return self.headID