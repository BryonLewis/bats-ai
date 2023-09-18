interface Options {
    audio: { enable: boolean};
    colors?: (steps: number) => string[];
    canvas: {
        width: (() => number) | number;
        height: (() => number) | number;
    }
}

interface AudioBufferStream {
    audioBuffer?: AudioBuffer,
    audioContext?: AudioContext,
    sourceNode?: AudioBufferSourceNode,
    analyser?: AnalyserNode | null,
    scriptNode?: ScriptProcessorNode | null,
    canvasContext?: SpectrogramCanvasContext

}

type SpectrogramCanvasContext = CanvasRenderingContext2D & { _tempContext: CanvasRenderingContext2D | null };

  function _isFunction(v: (()=> number )  | number) {
    return typeof v === 'function';
  }

  function _result(v: (() => number) | number): number {
    return (_isFunction(v) ? (v as () => number)() : v) as number;
  }

export default class Spectrogram {
    private _audioEnded: null | boolean;
    private _paused: null | boolean;
    private _pausedAt: number;
    private _startedAt: number;
    private _sources: {
        audioBufferStream: null | AudioBufferStream;
        userMediaStream: null | AudioBufferStream;
    };
    public audio: {enable: boolean};
    private _colors: string[];
    private _baseCanvas: HTMLCanvasElement;
    private _baseCanvasContext: SpectrogramCanvasContext | null;

    constructor(canvas: HTMLCanvasElement, options: Options) {
        this._baseCanvas = canvas;
        this._paused = false;
        this._audioEnded = false;
        this._pausedAt = 0;
        this._startedAt = 0;
        this._sources = {
            audioBufferStream: null,
            userMediaStream: null,
        };

        const baseCanvasOptions = options.canvas || {};

        this._baseCanvas = canvas;
        this._baseCanvasContext = this._baseCanvas.getContext('2d') as SpectrogramCanvasContext;


        this._baseCanvas.width = _result(baseCanvasOptions.width) || this._baseCanvas.width;
        this._baseCanvas.height = _result(baseCanvasOptions.height) || this._baseCanvas.height;
    
        window.onresize = () => {
          this._baseCanvas.width = _result(baseCanvasOptions.width) || this._baseCanvas.width;
          this._baseCanvas.height = _result(baseCanvasOptions.height) || this._baseCanvas.height;
        };
    

        let colors: string[]  = [];
        this.audio = options.audio || {};
        if (typeof options.colors === 'function') {
        colors = options.colors(275);
        } else {
        colors = this._generateDefaultColors(275);
        }
        this._colors = colors;
        if (this._baseCanvasContext) {
            this._baseCanvasContext.fillStyle = this._getColor(0);
            this._baseCanvasContext.fillRect(0, 0, this._baseCanvas.width, this._baseCanvas.height);
        }

    }

    private _init() {
        const source = this._sources.audioBufferStream;
        if (source && source.audioContext && source.sourceNode) {
            source.scriptNode = source.audioContext.createScriptProcessor(2048, 1, 1);
            source.scriptNode.connect(source.audioContext.destination);
            source.scriptNode.onaudioprocess = () => {
            if (source && source.analyser && source.canvasContext) {
                const array = new Uint8Array(source.analyser.frequencyBinCount);
                source.analyser.getByteFrequencyData(array);
            
                this._draw(array, source.canvasContext);
                }
            };
        
            source.sourceNode.onended = () => {
            this.stop();
            };
        
            source.analyser = source.audioContext.createAnalyser();
            source.analyser.smoothingTimeConstant = 0;
            source.analyser.fftSize = 1024;
        
            source.analyser.connect(source.scriptNode);
            source.sourceNode.connect(source.analyser);
            if (this.audio.enable) {
            source.sourceNode.connect(source.audioContext.destination);
            }
        }
      }
    
    private _draw(array: Uint8Array, canvasContext: SpectrogramCanvasContext) {
        if (this._paused) {
          return false;
        }
  
        const canvas = canvasContext.canvas;
        const width = canvas.width;
        const height = canvas.height;
        const tempCanvasContext = canvasContext._tempContext;
        if (tempCanvasContext) {
            const tempCanvas = tempCanvasContext.canvas;
            tempCanvasContext.drawImage(canvas, 0, 0, width, height);
    
            for (let i = 0; i < array.length; i++) {
            const value = array[i];
            canvasContext.fillStyle = this._getColor(value);
            if (this._audioEnded) {
                canvasContext.fillStyle = this._getColor(0);
            }
            canvasContext.fillRect(width - 1, height - i, 1, 1);
            }
    
            canvasContext.translate(-1, 0);
            // draw prev canvas before translation
            canvasContext.drawImage(tempCanvas, 0, 0, width, height, 0, 0, width, height);
            canvasContext.drawImage(tempCanvas, 0, 0, width, height, 0, 0, width, height);
            // reset transformation matrix
            canvasContext.setTransform(1, 0, 0, 1, 0, 0);
        }
  
        if (this._baseCanvasContext) {
            this._baseCanvasContext.drawImage(canvas, 0, 0, width, height);
        }
    }

    private _startMediaStreamDraw(analyser: AnalyserNode, canvasContext: SpectrogramCanvasContext) {
        window.requestAnimationFrame(this._startMediaStreamDraw.bind(this, analyser, canvasContext));
        const audioData = new Uint8Array(analyser.frequencyBinCount);
        analyser.getByteFrequencyData(audioData);
        this._draw(audioData, canvasContext);
      }


    public connectSource(audioBuffer: AudioBuffer, audioContext: AudioContext) {
        let source: AudioBufferStream  = this._sources.audioBufferStream || {};
    
        // clear current audio process
        if (source.scriptNode) {
            if (toString.call(source.scriptNode) === '[object ScriptProcessorNode]') {
            source.scriptNode.onaudioprocess = null;
            }
        }

    
        if (toString.call(audioBuffer) === '[object AudioBuffer]' && source.audioBuffer) {
          audioContext = (!audioContext && source.audioBuffer.context) || (!audioContext && source.audioContext) || audioContext;
    
          const sourceNode = audioContext.createBufferSource();
          sourceNode.buffer = audioBuffer;
    
          let canvasContext = source.canvasContext;
    
          if (!source.canvasContext) {
            const canvas = document.createElement('canvas');
            canvas.width = this._baseCanvas.width;
            canvas.height = this._baseCanvas.height;
            canvasContext = canvas.getContext('2d') as SpectrogramCanvasContext;
    
            const tempCanvas = document.createElement('canvas');
            tempCanvas.width = canvas.width;
            tempCanvas.height = canvas.height;
    
            canvasContext._tempContext = tempCanvas.getContext('2d');
          }
    
          source = {
            audioBuffer: audioBuffer,
            audioContext: audioContext,
            sourceNode: sourceNode,
            analyser: null,
            scriptNode: null,
            canvasContext: canvasContext
          };
    
          this._sources.audioBufferStream = source;
          this._init();
        }
    
        if (toString.call(audioBuffer) === '[object AnalyserNode]') {
          source = this._sources.userMediaStream || {};
          source.analyser = audioBuffer;
          this._sources.userMediaStream = source;
        }
      }

    public start(offset: number) {
        let source = this._sources.audioBufferStream;
        const sourceMedia = this._sources.userMediaStream;
    
        if (source && source.sourceNode) {
          source.sourceNode.start(0, offset||0);
          this._audioEnded = false;
          this._paused = false;
          this._startedAt = Date.now();
        }
    
        // media stream uses an analyser for audio data
        if (sourceMedia && sourceMedia.analyser) {
          source = sourceMedia;
          const canvas = document.createElement('canvas');
          canvas.width = this._baseCanvas.width;
          canvas.height = this._baseCanvas.height;
          const canvasContext = canvas.getContext('2d') as SpectrogramCanvasContext;
    
          const tempCanvas = document.createElement('canvas');
          tempCanvas.width = canvas.width;
          tempCanvas.height = canvas.height;
    
          canvasContext._tempContext = tempCanvas.getContext('2d');
          if (source?.analyser) {
            this._startMediaStreamDraw(source.analyser, canvasContext);
          }
        }
      }

    public stop() {
        const source = this._sources.audioBufferStream;
        if (source && source.sourceNode) {
          source.sourceNode.stop();
        }
        this._audioEnded = true;
      }
    
    public pause() {
        this.stop();
        this._paused = true;
        this._pausedAt += Date.now() - this._startedAt;
    }
    
    public resume(offset: number) {
        const source = this._sources.audioBufferStream;
        this._paused = false;
        if (this._pausedAt && source && source.audioBuffer && source.audioContext) {
          this.connectSource(source.audioBuffer, source.audioContext);
          this.start(offset || (this._pausedAt / 1000));
        }
    }

    public clear(canvasContext: SpectrogramCanvasContext) {
        const source = this._sources.audioBufferStream;
    
        this.stop();
        if (source?.scriptNode) {
            if (toString.call(source.scriptNode) === '[object ScriptProcessorNode]') {
            source.scriptNode.onaudioprocess = null;
            }
        }
        if (source && source.canvasContext) {
            canvasContext = canvasContext || source.canvasContext;
            const canvas = canvasContext.canvas;
            canvasContext.clearRect(0, 0, canvas.width, canvas.height);
            if (canvasContext._tempContext) {
                canvasContext._tempContext.clearRect(0, 0, canvas.width, canvas.height);
            }
            if (this._baseCanvasContext) {
            this._baseCanvasContext.clearRect(0, 0, canvas.width, canvas.height);
            }
        }
      }
    private _generateDefaultColors(steps: number) {
        const frequency = Math.PI / steps;
        const amplitude = 127;
        const center = 128;
        const slice = (Math.PI / 2) * 3.1;
        const colors = [];
    
        function toRGBString(v: number) {
          return 'rgba(' + [v,v,v,1].toString() + ')';
        }
    
        for (let i = 0; i < steps; i++) {
          const v = (Math.sin((frequency * i) + slice) * amplitude + center) >> 0;
    
          colors.push(toRGBString(v));
        }
    
        return colors;
    }


    

    private _getColor(index: number) {
        let color = this._colors[index>>0];
    
        if (typeof color === 'undefined') {
          color = this._colors[0];
        }
    
        return color;
    }
    
    
}