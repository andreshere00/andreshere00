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

      {/* Optional LinkedIn Avatar Safe-Zone Indicator (matches real LinkedIn avatar bounds) */}
      {showSafeZoneGuide && (
        <div className="absolute left-[64px] bottom-[-110px] w-[356px] h-[356px] rounded-full border-2 border-dashed border-sky-aqua/60 bg-deep-twilight/50 flex items-center justify-center z-30 pointer-events-none">
          <span className="text-sm uppercase tracking-wider text-frosted-blue font-medium px-6 pb-20 text-center">
            LinkedIn Profile Photo Zone
          </span>
        </div>
      )}

      {/* Main Content Container — Generous left margin (520px) + slight upward shift */}
      <div className="relative z-10 h-full w-full pl-[520px] pr-[56px] pb-[14px] flex items-center justify-between gap-8">
        {/* Center Column: Name, Motto, and Email */}
        <div className="flex flex-col justify-center space-y-3.5">
          {/* Name */}
          <h1 className="text-[66px] font-black tracking-tight text-white leading-[0.98]">
            Andrés Herencia
          </h1>

          {/* CV-style \xrfill tertiary horizontal bar + Motto */}
          <div className="space-y-3 pt-0.5">
            <div
              className="h-[5px] w-36 rounded-full"
              style={{
                background:
                  "linear-gradient(90deg, var(--turquoise-surf), var(--sky-aqua))",
              }}
            />
            <p className="text-[33px] font-bold text-light-cyan tracking-tight leading-[1.1]">
              {motto}
            </p>
          </div>

          {/* Email + Personal Emblem */}
          <div className="flex items-center gap-3.5 pt-1">
            <Mail className="w-6 h-6 text-sky-aqua shrink-0 stroke-[2.2]" />
            <span className="text-[25px] font-medium text-white tracking-normal leading-none">
              andresherencia2000@gmail.com
            </span>
            <img
              src="/assets/logo-andres.png"
              alt="Andrés Herencia Emblem"
              className="w-8 h-8 object-contain brightness-0 invert opacity-95 ml-1"
            />
          </div>
        </div>

        {/* Right Column: Uncropped Official AWS Hexagonal Badges */}
        <div className="flex items-center gap-3.5 shrink-0">
          <img
            src="/assets/aws-mla.png"
            alt="AWS Certified Machine Learning Engineer – Associate"
            className="w-[210px] h-[210px] object-contain drop-shadow-[0_10px_22px_rgba(0,0,0,0.45)]"
          />
          <img
            src="/assets/aws-saa.png"
            alt="AWS Certified Solutions Architect – Associate"
            className="w-[210px] h-[210px] object-contain drop-shadow-[0_10px_22px_rgba(0,0,0,0.45)]"
          />
        </div>
      </div>
    </div>
  );
};
