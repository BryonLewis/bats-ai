
  
export default function AudioBufferSlice(
    buffer: AudioBuffer,
    begin = 0,
    end: number,
    callback: (err: Error | null, buff: AudioBuffer | undefined) => void,
) {
  
      let error: Error | null = null;
  
      const duration = buffer.duration;
      const channels = buffer.numberOfChannels;
      const rate = buffer.sampleRate;
  
      if (typeof end === 'function') {
        callback = end;
        end = duration;
      }
  
      // milliseconds to seconds
      begin = begin/1000;
      if (end > begin) {
        end = end/1000;
      } else {
        end = buffer.duration;
      }
  
      if (begin < 0) {
        error = new RangeError('begin time must be greater than 0');
      }
  
      if (end > duration) {
        error = new RangeError('end time must be less than or equal to ' + duration);
      }
  
      if (typeof callback !== 'function') {
        error = new TypeError('callback must be a function');
      }
  
      const startOffset = rate * begin;
      const endOffset = rate * end;
      const frameCount = endOffset - startOffset;
      let newArrayBuffer;
  
      try {
        const audioContext = new AudioContext();
  
        newArrayBuffer = audioContext.createBuffer(channels, endOffset - startOffset, rate);
        const anotherArray = new Float32Array(frameCount);
        const offset = 0;
  
        for (let channel = 0; channel < channels; channel++) {
          buffer.copyFromChannel(anotherArray, channel, startOffset);
          newArrayBuffer.copyToChannel(anotherArray, channel, offset);
        }
      } catch(e) {
        error = e as Error;
      }
  
      callback(error, newArrayBuffer);
}
  