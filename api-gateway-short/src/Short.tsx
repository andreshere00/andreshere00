import React from "react";
import {
  AbsoluteFill, Sequence, interpolate, spring, useCurrentFrame, useVideoConfig,
} from "remotion";

export const FPS = 30;
export const TOTAL_SECONDS = 60;

const C = {
  bg: "#0b1020", panel: "#161d36", accent: "#4f8cff", green: "#2ee6a6",
  warn: "#ff5d73", yellow: "#ffd166", text: "#f4f6ff", dim: "#8d97c4",
};
const FONT = "'Inter','Helvetica Neue',Arial,sans-serif";
const sec = (s: number): number => Math.round(s * FPS);

const usePop = (delaySec = 0): number => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  return spring({frame: frame - sec(delaySec), fps, config: {damping: 12, stiffness: 180}});
};

const Pop: React.FC<{delay?: number; style?: React.CSSProperties; children: React.ReactNode}> = (
  {delay = 0, style, children},
) => {
  const s = usePop(delay);
  return (
    <div style={{opacity: Math.min(1, s * 1.5), ...style}}>
      {children}
    </div>
  );
};

const Title: React.FC<{children: React.ReactNode; color?: string}> = ({children, color}) => (
  <div style={{
    position: "absolute", top: 170, left: 90, right: 190, fontSize: 84, fontWeight: 900,
    lineHeight: 1.05, color: color ?? C.text, letterSpacing: -2, fontFamily: FONT,
  }}>{children}</div>
);

const Caption: React.FC<{children: React.ReactNode}> = ({children}) => {
  const s = usePop(0);
  return (
    <div style={{
      position: "absolute", left: 90, right: 190, top: 1330, textAlign: "center",
      fontSize: 52, fontWeight: 800, color: C.text, fontFamily: FONT, lineHeight: 1.2,
      opacity: s, transform: `translateY(${(1 - s) * 30}px)`,
    }}>{children}</div>
  );
};

const Box: React.FC<{x: number; y: number; w: number; h: number; label: string; color?: string;
  size?: number}> = ({x, y, w, h, label, color = C.panel, size = 34}) => (
  <div style={{
    position: "absolute", left: x, top: y, width: w, height: h, background: color,
    borderRadius: 22, display: "flex", alignItems: "center", justifyContent: "center",
    color: C.text, fontSize: size, fontWeight: 800, fontFamily: FONT,
    border: `3px solid ${color === C.panel ? "#2a3566" : "transparent"}`,
  }}>{label}</div>
);

const Line: React.FC<{x1: number; y1: number; x2: number; y2: number; color?: string;
  progress?: number; width?: number}> = ({x1, y1, x2, y2, color = C.dim, progress = 1, width = 4}) => (
  <svg style={{position: "absolute", inset: 0, width: 1080, height: 1920, pointerEvents: "none"}}>
    <line x1={x1} y1={y1} x2={x1 + (x2 - x1) * progress} y2={y1 + (y2 - y1) * progress}
      stroke={color} strokeWidth={width} strokeLinecap="round" />
  </svg>
);

const SERVICES = ["Users", "Orders", "Pay", "Stock", "Mail", "Search"];
const svcPos = (i: number): {x: number; y: number} => ({x: 90 + (i % 3) * 280, y: 980 + Math.floor(i / 3) * 150});

const Hook: React.FC = () => (
  <AbsoluteFill>
    <Title>50 microservices.<br /><span style={{color: C.accent}}>ONE door.</span></Title>
    <Box x={290} y={560} w={420} h={180} label="API GATEWAY" color={C.accent} size={44} />
    <Box x={400} y={420} w={200} h={90} label="App" size={36} />
    {[0, 1, 2, 3, 4, 5].map((i) => {
      const x = 130 + i * 140;
      return <React.Fragment key={i}>
        <Line x1={500} y1={740} x2={x + 50} y2={900} color="#2a3566" />
        <div style={{position: "absolute", left: x, top: 900, width: 100, height: 100,
          borderRadius: 24, background: C.panel, border: "3px solid #2a3566"}} />
      </React.Fragment>;
    })}
    <Line x1={500} y1={510} x2={500} y2={560} color={C.green} />
    <Caption>Your phone talks to one door.</Caption>
  </AbsoluteFill>
);

const Problem: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Title color={C.warn}>No gateway = chaos</Title>
      <Box x={390} y={420} w={220} h={100} label="Client" size={40} />
      {SERVICES.map((n, i) => {
        const p = svcPos(i);
        const prog = interpolate(frame, [sec(0.8 + i * 0.4), sec(1.4 + i * 0.4)], [0, 1],
          {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
        return <React.Fragment key={n}>
          <Line x1={500} y1={520} x2={p.x + 110} y2={p.y} color={C.warn} progress={prog} />
          <Pop delay={0.8 + i * 0.4}>
            <Box x={p.x} y={p.y} w={220} h={100} label={n} />
          </Pop>
        </React.Fragment>;
      })}
      <Caption>Every client needs every address, auth, and protocol.</Caption>
    </AbsoluteFill>
  );
};

const Single: React.FC = () => (
  <AbsoluteFill>
    <Title color={C.green}>One entry point</Title>
    <Pop><Box x={390} y={420} w={220} h={100} label="Client" size={40} /></Pop>
    <Line x1={500} y1={520} x2={500} y2={640} color={C.green} />
    <Pop delay={0.5}><Box x={290} y={640} w={420} h={140} label="API GATEWAY" color={C.accent} size={42} /></Pop>
    {SERVICES.map((n, i) => {
      const p = svcPos(i);
      return <React.Fragment key={n}>
        <Pop delay={1 + i * 0.25}>
          <Line x1={500} y1={780} x2={p.x + 110} y2={p.y} color={C.accent} />
          <Box x={p.x} y={p.y} w={220} h={100} label={n} />
        </Pop>
      </React.Fragment>;
    })}
    <Caption>Like the receptionist of a big building.</Caption>
  </AbsoluteFill>
);

const FEATURES: {icon: string; name: string; desc: string}[] = [
  {icon: "🧭", name: "Routing", desc: "/users → Users\n/orders → Orders"},
  {icon: "🔐", name: "Authentication", desc: "Checks the token once"},
  {icon: "🚦", name: "Rate limiting", desc: "Blocks abuse and spam"},
  {icon: "⚡", name: "Caching", desc: "Repeat requests answered instantly"},
  {icon: "⚖️", name: "Load balancing", desc: "Spreads traffic across instances"},
  {icon: "🧩", name: "Aggregation", desc: "Many calls, one response"},
  {icon: "📊", name: "Monitoring", desc: "One place to see all traffic"},
];
const FEATURE_SECS = 23 / FEATURES.length;

const Features: React.FC = () => {
  const frame = useCurrentFrame();
  const idx = Math.min(FEATURES.length - 1, Math.floor(frame / sec(FEATURE_SECS)));
  const f = FEATURES[idx];
  const local = frame - idx * sec(FEATURE_SECS);
  const s = spring({frame: local, fps: FPS, config: {damping: 11, stiffness: 190}});
  return (
    <AbsoluteFill>
      <Title>What it does</Title>
      <div style={{position: "absolute", left: 90, top: 480, width: 800, display: "flex",
        justifyContent: "center", gap: 14}}>
        {FEATURES.map((_, i) => (
          <div key={i} style={{width: 70, height: 12, borderRadius: 6,
            background: i <= idx ? C.accent : "#2a3566"}} />
        ))}
      </div>
      <div style={{
        position: "absolute", left: 90, top: 560, width: 800, height: 640, borderRadius: 48,
        background: C.panel, border: "3px solid #2a3566", display: "flex", flexDirection: "column",
        alignItems: "center", justifyContent: "center", gap: 24, transform: `scale(${0.8 + 0.2 * s})`,
        opacity: Math.min(1, s * 2), fontFamily: FONT,
      }}>
        <div style={{fontSize: 220}}>{f.icon}</div>
        <div style={{fontSize: 80, fontWeight: 900, color: C.accent}}>{idx + 1}. {f.name}</div>
        <div style={{fontSize: 44, fontWeight: 700, color: C.text, textAlign: "center",
          whiteSpace: "pre-line", padding: "0 30px"}}>{f.desc}</div>
      </div>
    </AbsoluteFill>
  );
};

const FLOW = ["Client", "Gateway", "Auth + limits", "Service"];

const Flow: React.FC = () => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [sec(0.5), sec(4.5)], [0, 3], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  const ys = FLOW.map((_, i) => 450 + i * 190);
  const dotY = interpolate(t, [0, 1, 2, 3], ys.map((y) => y + 55));
  return (
    <AbsoluteFill>
      <Title>The flow</Title>
      {FLOW.map((n, i) => (
        <React.Fragment key={n}>
          {i > 0 && <Line x1={500} y1={ys[i - 1] + 110} x2={500} y2={ys[i]} color={C.dim} />}
          <Pop delay={i * 0.3}>
            <Box x={290} y={ys[i]} w={420} h={110} label={n}
              color={i === 1 ? C.accent : C.panel} size={40} />
          </Pop>
        </React.Fragment>
      ))}
      <div style={{position: "absolute", left: 726, top: dotY - 25, width: 50, height: 50,
        borderRadius: 25, background: C.yellow, boxShadow: `0 0 30px ${C.yellow}`}} />
      <Caption>The response travels back the same way.</Caption>
    </AbsoluteFill>
  );
};

const TOOLS = ["AWS API Gateway", "Kong", "NGINX", "Apigee", "Azure API Mgmt"];
const Tools: React.FC = () => (
  <AbsoluteFill>
    <Title>Popular tools</Title>
    {TOOLS.map((n, i) => (
      <Pop key={n} delay={i * 0.6}>
        <Box x={140} y={420 + i * 150} w={700} h={115} label={n} size={46}
          color={i % 2 ? C.panel : "#1e2850"} />
      </Pop>
    ))}
  </AbsoluteFill>
);

const Cta: React.FC = () => (
  <AbsoluteFill>
    <Title color={C.accent}>One door,<br />many services.</Title>
    <Pop delay={0.3} style={{position: "absolute", left: 90, right: 190, top: 700,
      textAlign: "center", fontSize: 64, fontWeight: 800, color: C.text, fontFamily: FONT}}>
      Follow for more backend concepts in 60 seconds
    </Pop>
    <Pop delay={0.8}><Box x={190} y={1000} w={600} h={120}
      label="#backend #apigateway" color={C.accent} size={44} /></Pop>
  </AbsoluteFill>
);

const SCENES: {from: number; to: number; node: React.ReactNode}[] = [
  {from: 0, to: 3, node: <Hook />},
  {from: 3, to: 12, node: <Problem />},
  {from: 12, to: 22, node: <Single />},
  {from: 22, to: 45, node: <Features />},
  {from: 45, to: 52, node: <Flow />},
  {from: 52, to: 57, node: <Tools />},
  {from: 57, to: 59, node: <Cta />},
  {from: 59, to: 60, node: <Hook />},
];

export const Short: React.FC = () => {
  const frame = useCurrentFrame();
  const drift = interpolate(frame, [0, sec(TOTAL_SECONDS)], [0, 120]);
  return (
    <AbsoluteFill style={{background: C.bg, fontFamily: FONT}}>
      <div style={{position: "absolute", width: 900, height: 900, borderRadius: 450, left: -200,
        top: 900 - drift, background: "radial-gradient(#4f8cff33, transparent 70%)"}} />
      {SCENES.map((s, i) => (
        <Sequence key={i} from={sec(s.from)} durationInFrames={sec(s.to - s.from)}>{s.node}</Sequence>
      ))}
    </AbsoluteFill>
  );
};
