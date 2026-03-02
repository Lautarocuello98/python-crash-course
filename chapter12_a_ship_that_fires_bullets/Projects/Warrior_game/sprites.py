# sprites.py
import pygame

def load_sheet(path: str) -> pygame.Surface:
    img = pygame.image.load(path).convert_alpha()
    return img

def slice_sheet(sheet: pygame.Surface, frame_w: int, frame_h: int):
    """Corta un spritesheet en grilla. Devuelve lista de frames."""
    frames = []
    sheet_w, sheet_h = sheet.get_size()
    cols = sheet_w // frame_w
    rows = sheet_h // frame_h

    for r in range(rows):
        for c in range(cols):
            rect = pygame.Rect(c * frame_w, r * frame_h, frame_w, frame_h)
            frame = sheet.subsurface(rect).copy()
            frames.append(frame)
    return frames

def scale_frames(frames, scale: float):
    if scale == 1.0:
        return frames
    out = []
    for f in frames:
        w, h = f.get_size()
        out.append(pygame.transform.scale(f, (int(w * scale), int(h * scale))))
    return out