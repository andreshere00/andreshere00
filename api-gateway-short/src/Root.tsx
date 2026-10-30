import {Composition} from "remotion";
import {Short, FPS, TOTAL_SECONDS} from "./Short";

export const Root: React.FC = () => (
  <Composition
    id="Short"
    component={Short}
    durationInFrames={FPS * TOTAL_SECONDS}
    fps={FPS}
    width={1080}
    height={1920}
  />
);
