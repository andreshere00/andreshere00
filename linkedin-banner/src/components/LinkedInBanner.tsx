import React from "react";
import { Mail, MapPin, CheckCircle2, Sparkles, Cloud, Cpu } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";

export interface LinkedInBannerProps {
  motto?: string;
  subtitle?: string;
  showSafeZoneGuide?: boolean;
}

export const LinkedInBanner: React.FC<LinkedInBannerProps> = ({
  motto = "Forward Deployed AI Engineer",
  subtitle = "2x AWS-Certified  •  +3 years designing & building AI-driven products",
  showSafeZoneGuide = false,
}) => {
  return (
    <div
      id="linkedin-banner-canvas"
      className="relative w-[1584px] h-[396px] overflow-hidden select-none font-sans text-white"
      style={{
        background:
          "linear-gradient(115deg, var(--deep-twilight) 0%, #02205c 42%, var(--french-blue) 78%, var(--bright-teal-blue) 100%)",
        fontFamily: "'Roboto', sans-serif",
      }}
    >
      {/* Subtle architectural grid & radial glow matching CV header shading */}
      <div
        className="absolute inset-0 opacity-20 pointer-events-none"
        style={{
          backgroundImage:
            "radial-gradient(circle at 75% 30%, var(--turquoise-surf) 0%, transparent 55%), radial-gradient(circle at 20% 80%, var(--bright-teal-blue) 0%, transparent 45%)",
        }}
      />

      {/* Flowing topographic / neural wave lines (top-left & bottom-right) */}
      <svg
        className="absolute inset-0 w-full h-full pointer-events-none"
        viewBox="0 0 1584 396"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <linearGradient id="waveGradLeft" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#48cae4" stopOpacity="0.45" />
            <stop offset="50%" stopColor="#00b4d8" stopOpacity="0.22" />
            <stop offset="100%" stopColor="#0077b6" stopOpacity="0.0" />
          </linearGradient>
          <linearGradient id="waveGradRight" x1="100%" y1="100%" x2="0%" y2="0%">
            <stop offset="0%" stopColor="#90e0ef" stopOpacity="0.4" />
            <stop offset="55%" stopColor="#0096c7" stopOpacity="0.2" />
            <stop offset="100%" stopColor="#023e8a" stopOpacity="0.0" />
          </linearGradient>
        </defs>

        {/* Top-left wave bundle */}
        {[0, 12, 24, 36, 48, 60, 72, 84].map((offset, idx) => (
          <path
            key={`tl-${idx}`}
            d={`M ${-60 + offset * 0.5} ${340 - offset * 1.4} C ${160 + offset} ${260 - offset}, ${240 - offset} ${90 + offset}, ${540 + offset * 1.8} ${-30 + offset * 0.5}`}
            stroke="url(#waveGradLeft)"
            strokeWidth={1.6}
          />
        ))}

        {/* Bottom-right wave bundle */}
        {[0, 12, 24, 36, 48, 60, 72, 84].map((offset, idx) => (
          <path
            key={`br-${idx}`}
            d={`M ${1080 + offset * 1.5} ${430 - offset * 0.5} C ${1260 - offset} ${310 + offset}, ${1390 + offset} ${190 - offset}, ${1640 - offset * 0.5} ${90 + offset * 1.3}`}
            stroke="url(#waveGradRight)"
            strokeWidth={1.6}
          />
        ))}
      </svg>

      {/* Optional LinkedIn Avatar Safe-Zone Indicator */}
      {showSafeZoneGuide && (
        <div className="absolute left-[36px] bottom-[-40px] w-[268px] h-[268px] rounded-full border-2 border-dashed border-sky-aqua/60 bg-deep-twilight/50 flex items-center justify-center z-30 pointer-events-none">
          <span className="text-xs uppercase tracking-wider text-frosted-blue font-medium px-4 text-center">
            LinkedIn Profile Photo Zone
          </span>
        </div>
      )}

      {/* Main Content Container (positioned to the right of LinkedIn's profile photo overlay) */}
      <div className="relative z-10 h-full w-full pl-[355px] pr-[52px] py-[34px] flex items-center justify-between gap-8">
        {/* Left/Center Column: Name, CV horizontal rule accent, Motto & Role Pills */}
        <div className="flex flex-col justify-between h-full max-w-[760px] py-1">
          {/* Top Status Pill matching CV header */}
          <div className="flex items-center gap-2.5">
            <Badge
              variant="outline"
              className="border-sky-aqua/40 bg-deep-twilight/60 text-light-cyan px-3 py-1 text-xs font-medium tracking-wide uppercase backdrop-blur-sm flex items-center gap-1.5"
            >
              <Sparkles className="w-3.5 h-3.5 text-sky-aqua" />
              AI Architecture & Agentic Systems
            </Badge>
            <Badge
              variant="outline"
              className="border-turquoise-surf/30 bg-french-blue/40 text-frosted-blue-2 px-3 py-1 text-xs font-normal tracking-wide backdrop-blur-sm flex items-center gap-1.5"
            >
              <MapPin className="w-3.5 h-3.5 text-turquoise-surf" />
              Madrid, Spain
            </Badge>
          </div>

          {/* Center Identity Block */}
          <div className="my-auto space-y-3">
            <div className="flex items-baseline gap-4">
              <h1 className="text-[54px] font-black tracking-tight text-white leading-none uppercase drop-shadow-sm">
                Andrés Herencia
              </h1>
              <span className="w-3 h-3 rounded-full bg-turquoise-surf inline-block shrink-0 shadow-[0_0_12px_#00b4d8]" />
            </div>

            {/* CV-style \xrfill tertiary horizontal bar */}
            <div className="flex items-center gap-3">
              <div
                className="h-[3px] w-24 rounded-full"
                style={{
                  background:
                    "linear-gradient(90deg, var(--turquoise-surf), var(--sky-aqua))",
                }}
              />
              <div className="h-[1px] flex-1 bg-gradient-to-r from-sky-aqua/50 via-bright-teal-blue/30 to-transparent" />
            </div>

            {/* Motto */}
            <p className="text-[24px] font-bold text-light-cyan tracking-normal leading-snug">
              {motto}
            </p>
            <p className="text-[16px] font-normal text-frosted-blue/90 tracking-wide">
              {subtitle}
            </p>
          </div>

          {/* Bottom Tech / Domain Pill Bar matching CV highlights */}
          <div className="flex items-center gap-2 text-xs text-frosted-blue-2/90">
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-deep-twilight/55 border border-bright-teal-blue/40">
              <Cpu className="w-3.5 h-3.5 text-sky-aqua" />
              LLMs · RAG · MCP Servers
            </span>
            <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md bg-deep-twilight/55 border border-bright-teal-blue/40">
              <Cloud className="w-3.5 h-3.5 text-sky-aqua" />
              AWS Event-Driven & Serverless AI
            </span>
          </div>
        </div>

        {/* Right Column: Official AWS Certification Badges + Contact & Personal Icon */}
        <div className="flex flex-col items-end justify-between h-full shrink-0 py-1">
          {/* AWS Certifications Card (shadcn Card) */}
          <Card className="bg-deep-twilight/55 border-sky-aqua/30 backdrop-blur-md px-5 py-3.5 rounded-2xl shadow-lg flex items-center gap-5">
            <div className="flex flex-col items-end pr-1">
              <div className="flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-sky-aqua">
                <CheckCircle2 className="w-3.5 h-3.5 text-turquoise-surf" />
                <span>2x AWS Certified</span>
              </div>
              <span className="text-[11px] text-frosted-blue/85 mt-0.5">
                Solutions Architect & ML Engineer
              </span>
              <span className="text-[10px] text-frosted-blue/60 font-light">
                Associate Level
              </span>
            </div>

            <Separator
              orientation="vertical"
              className="h-16 bg-sky-aqua/25"
            />

            <div className="flex items-center gap-3.5">
              <div className="group relative flex flex-col items-center">
                <img
                  src="/assets/aws-mla.png"
                  alt="AWS Certified Machine Learning Engineer – Associate"
                  className="w-[104px] h-[104px] object-contain drop-shadow-[0_4px_10px_rgba(0,180,216,0.3)]"
                />
              </div>
              <div className="group relative flex flex-col items-center">
                <img
                  src="/assets/aws-saa.png"
                  alt="AWS Certified Solutions Architect – Associate"
                  className="w-[104px] h-[104px] object-contain drop-shadow-[0_4px_10px_rgba(0,180,216,0.3)]"
                />
              </div>
            </div>
          </Card>

          {/* Bottom-Right Contact & Personal Logo Row */}
          <div className="flex items-center gap-3.5 bg-deep-twilight/65 border border-sky-aqua/30 backdrop-blur-md px-4 py-2 rounded-xl shadow-md">
            <div className="flex items-center gap-2 text-sm text-light-cyan font-medium tracking-wide">
              <div className="w-7 h-7 rounded-lg bg-bright-teal-blue/40 border border-sky-aqua/40 flex items-center justify-center">
                <Mail className="w-4 h-4 text-sky-aqua" />
              </div>
              <span>andresherencia2000@gmail.com</span>
            </div>

            <Separator
              orientation="vertical"
              className="h-6 bg-sky-aqua/30"
            />

            {/* Attached personal cloud-book icon rendered in white/cyan */}
            <div
              className="w-8 h-8 flex items-center justify-center"
              title="Andrés Herencia — Personal Emblem"
            >
              <img
                src="/assets/logo-andres.png"
                alt="Andrés Herencia Emblem"
                className="w-7 h-7 object-contain brightness-0 invert opacity-95"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
