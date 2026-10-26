import React from "react";
import { Mail } from "lucide-react";

export interface LinkedInBannerProps {
  motto?: string;
  showSafeZoneGuide?: boolean;
}

export const LinkedInBanner: React.FC<LinkedInBannerProps> = ({
  motto = "Forward Deployed AI Engineer",
  showSafeZoneGuide = false,
}) => {
  return (
    <div
      id="linkedin-banner-canvas"
      className="relative w-[1584px] h-[396px] overflow-hidden select-none font-sans text-white"
      style={{
        background:
          "linear-gradient(100deg, var(--deep-twilight) 0%, #02205c 58%, var(--french-blue) 100%)",
        fontFamily: "'Roboto', sans-serif",
      }}
    >
      {/* Subtle top-right radial accent matching CV TikZ header shading */}
      <div
        className="absolute inset-0 opacity-25 pointer-events-none"
        style={{
          backgroundImage:
            "radial-gradient(circle at 82% 50%, var(--bright-teal-blue) 0%, transparent 55%)",
        }}
      />

      {/* Optional LinkedIn Avatar Safe-Zone Indicator */}
      {showSafeZoneGuide && (
        <div className="absolute left-[36px] bottom-[-40px] w-[268px] h-[268px] rounded-full border-2 border-dashed border-sky-aqua/60 bg-deep-twilight/50 flex items-center justify-center z-30 pointer-events-none">
          <span className="text-sm uppercase tracking-wider text-frosted-blue font-medium px-4 text-center">
            LinkedIn Profile Photo Zone
          </span>
        </div>
      )}

      {/* Main Content Container — Balanced 2-Column Layout with Bold Typography */}
      <div className="relative z-10 h-full w-full pl-[336px] pr-[48px] flex items-center justify-between gap-8">
        {/* Left/Center Column: Name, Motto, and Email */}
        <div className="flex flex-col justify-center space-y-5">
          {/* Name */}
          <h1 className="text-[92px] font-black tracking-tight text-white leading-[0.95]">
            Andrés Herencia
          </h1>

          {/* CV-style \xrfill tertiary horizontal bar + Motto */}
          <div className="space-y-4 pt-1">
            <div
              className="h-[6px] w-48 rounded-full"
              style={{
                background:
                  "linear-gradient(90deg, var(--turquoise-surf), var(--sky-aqua))",
              }}
            />
            <p className="text-[46px] font-bold text-light-cyan tracking-tight leading-[1.08]">
              {motto}
            </p>
          </div>

          {/* Email + Personal Emblem */}
          <div className="flex items-center gap-4 pt-2">
            <Mail className="w-9 h-9 text-sky-aqua shrink-0 stroke-[2.25]" />
            <span className="text-[36px] font-medium text-white tracking-normal leading-none">
              andresherencia2000@gmail.com
            </span>
            <img
              src="/assets/logo-andres.png"
              alt="Andrés Herencia Emblem"
              className="w-11 h-11 object-contain brightness-0 invert opacity-95 ml-1"
            />
          </div>
        </div>

        {/* Right Column: Large, Clear Official AWS Certification Badges */}
        <div className="flex items-center gap-4 shrink-0">
          <img
            src="/assets/aws-mla.png"
            alt="AWS Certified Machine Learning Engineer – Associate"
            className="w-[228px] h-[228px] object-contain drop-shadow-[0_12px_28px_rgba(0,0,0,0.5)]"
          />
          <img
            src="/assets/aws-saa.png"
            alt="AWS Certified Solutions Architect – Associate"
            className="w-[228px] h-[228px] object-contain drop-shadow-[0_12px_28px_rgba(0,0,0,0.5)]"
          />
        </div>
      </div>
    </div>
  );
};
