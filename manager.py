#Camo项目，人脸跟踪和图像处理
import cv2
import numpy
import time
class CaptureManager(object):
    def __init__(self,capture,previewWindowManager=None,shouldMirrorPreview=False):
        self.previewWindowManager=previewWindowManager
        self.shouldMirrorPreview=shouldMirrorPreview

        self._capture=capture
        self._channel=0
        self._enteredFrame=False

        self._frame=None
        self._imageFileName=None
        self._videoFileName=None
        self._videoEncoding=None
        self._videoWriter=None

        self._startTime=None
        self._framesElapsed=0#python2中有long类型，python3中没有long类型
        self._fpsEstimate=None

        @property
        def channel(self):
            return self._channel
        @channel.setter
        def channel(self,value):
            if self._channel!=value:
                self._channel=value
                self._frame=None

        @property
        def frame(self):
            if self._enteredFrame and self._frame is None:
                _,self._frame=self._capture.retrieve()
            return self._frame

        @property
        def isWritingImage(self):
            return self._imageFileName is not None

        @property
        def isWritingVideo(self):
            return self._videoFileName is not None

        def enterFrame(self):
            "capture the next frame,if any."
            assert not self._enteredFrame,"previous enterFrame() had no matching exitFrame()"
            if self._capture is not None:
                self._enteredFrame=self._capture.grab()

        def exitFrame(self):
            "Draw to the window,write to files.release the frame."
            if self.frame is not None:
                self._enteredFrame=False
                return
            if self._framesElapsed==0:
                self.startTime=time.time()
            else:
                tiemElapsed=time.timr()-self._startTime
            self._fpsEstimate=self._framesElapsed/tiemElapsed
        self._frame+=1
        if self.previewWindowManager is not None:
            if self.shouldMirrorPreview:
                mirroredFrame=numpy.fliplr(self._frame).copy()
                self.previewWindowManager.show(mirroredFrame)
            else:
                self.previewWindowManager.show(self._frame)
            #write to the image file,if any
            if self.isWritignImage:
                cv2.imwrite(self._imageFileName,self._frame)
                self._imageFileName=None

            #write to the video file ,if any
            self._writeVideoFrame()
            #release the frame
            self._frame=None
            self._enteredFrame=False
        def writeImage(self,filename):
            """write the next exited frame to an image file."""
            self._imageFileName=filename
        def startWritingVideo(self,filename,encoding=cv2.VideoWriter_fourcc("I","4","2","0")):
            """Start writing exited frames to a video file."""
            self._videoFileName=filename
            self._videoEncoding=encoding
        def stopWritingVideo(self):
            """stop writing exited frames to a video file."""
            self._videoFileName=None
            self._videoEncoding=None
            self._videoWriter=None

        def _writeVideoFrame(self):
            if not self.isWritingVideo:
                return
            if self._videoWriter is None:
                fps=self._capture.get(cv2.CAP_PROP_FPS)
                if fps==0.0:
                    # the capture's fps is unknown so use an estimate.
                    if self._framesElapsed<20:
                        #wait until more frames elapses so that the estimate is more stable.
                        return
                    else:
                        fps=self._fpsEstimate
                size=(int(self._capture.get(cv2.CAP_PROP_FRAME_WIDTH)),int(self._capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
                self._videoWriter=cv2.VideoWriter(self._videoFileName,self._videoEncoding,fps,size)
                self._videoWriter.write(self._frame)
    class WindowManager(object):
        def __init__(self,windowName,keypressCallback=None):
            self.keypressCallback=keypressCallback
            self.windowName=windowName
            self._isWindowCreated=False

            @property
            def isWindowCreated(self):
                return self.isWindowCreated

            def createWindow(self):
                cv2.namedWindow(self._windowName)
                self._isWindowCreated=True

            def show(self,frame):
                cv2.imshow(self._windowName,frame)

            def destoryWindow(self):
                cv2.destroyWindow(self._windowName)
                self._isWindowCreated=False

            def processEvents(self):
                keycode=cv2.waitKey(1)
                if self.keypressCallback is not None and keycode!=-1:
                    keycode&=0xFF
                    self.keypressCallback(keycode)

