class PixelDisplay {

    private static readonly ROW_COUNT = 32;
    private static readonly COLUMN_COUNT = 64;
    private static readonly FOREGROUND_COLOR = '0xFFFFFF';
    private static readonly BACKGROUND_COLOR = '0x000000';

    private readonly canvas: HTMLCanvasElement;
    private readonly ctx: CanvasRenderingContext2D;
    private readonly pixel_width: number;
    private readonly pixel_height: number;

    constructor(canvas: HTMLCanvasElement) {
        this.canvas = canvas;
        this.ctx = <CanvasRenderingContext2D> canvas.getContext('2D');
        this.pixel_width = this.canvas.width / PixelDisplay.COLUMN_COUNT;
        this.pixel_height = this.canvas.height / PixelDisplay.ROW_COUNT;
        this.clear();
    }

    setPixel(x: number, y: number, state: boolean): void {
        this.ctx.fillStyle = state ? PixelDisplay.FOREGROUND_COLOR : PixelDisplay.BACKGROUND_COLOR;
        this.ctx.fillRect(x * this.pixel_width, y * this.pixel_height,
                this.pixel_width, this.pixel_height);
    }

    setPixels(pixels: [number, number, boolean][]): void {
        for (let i = 0; i < pixels.length; i++) {
            let [x, y, state] = pixels[i];
            this.setPixel(x, y, state);
        }
    }

    clear() {
        this.ctx.fillStyle = PixelDisplay.BACKGROUND_COLOR;
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    }
}