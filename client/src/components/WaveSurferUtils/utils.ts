
export interface AudioAnnotation {
    start: number; //ms
    end: number; //ms
    minFreq: number; //Hz
    maxFreq: number; //Hz
}
// Draw Annotations

function drawAnnotation(canvas: HTMLCanvasElement, range: {duration: number, minFreq: number, maxFreq: number}, annotation: AudioAnnotation)  {
    if (canvas) {
        // First we need to scale the visible area to duration and frequency range;
        const timeScale = canvas.width / range.duration;
        const freqScale = canvas.height / (range.maxFreq - range.minFreq);
        const ctx = canvas.getContext('2d');
        if (ctx) {
            ctx.strokeStyle = 'red';
            ctx.lineWidth = Math.max(canvas.width, canvas.height) / 500.0;
            const x = annotation.start * timeScale;
            const y = canvas.height - (annotation.minFreq * freqScale);
            const width = annotation.end * timeScale - x;
            const height = (canvas.height -(annotation.maxFreq * freqScale)) - y;
            //ctx.clearRect(x, y, width, height);
            ctx.strokeRect(x, y, width, height);
        }

    }
}

export {
    drawAnnotation,
};