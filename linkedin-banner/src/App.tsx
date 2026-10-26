import { useState } from "react";
import { LinkedInBanner } from "@/components/LinkedInBanner";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Eye, Sparkles, Palette, Check } from "lucide-react";

const MOTTO_PRESETS = [
  {
    label: "CV Header (Current)",
    motto: "Forward Deployed AI Engineer",
    subtitle: "2x AWS-Certified  •  +3 years designing & building AI-driven products",
  },
  {
    label: "Classic ML & Solutions Architect",
    motto: "Machine Learning Engineer & AI Solutions Architect",
    subtitle: "Designing & building scalable GenAI, RAG, and event-driven cloud architectures",
  },
];

const PALETTE_SWATCHES = [
  { name: "--deep-twilight", hex: "#03045eff" },
  { name: "--french-blue", hex: "#023e8aff" },
  { name: "--bright-teal-blue", hex: "#0077b6ff" },
  { name: "--blue-green", hex: "#0096c7ff" },
  { name: "--turquoise-surf", hex: "#00b4d8ff" },
  { name: "--sky-aqua", hex: "#48cae4ff" },
  { name: "--frosted-blue", hex: "#90e0efff" },
  { name: "--frosted-blue-2", hex: "#ade8f4ff" },
  { name: "--light-cyan", hex: "#caf0f8ff" },
];

export function App() {
  const isBannerOnly =
    typeof window !== "undefined" &&
    new URLSearchParams(window.location.search).get("banner") === "1";
  const presetParam =
    typeof window !== "undefined"
      ? Number(new URLSearchParams(window.location.search).get("preset") || "0")
      : 0;

  const [presetIdx, setPresetIdx] = useState(presetParam);
  const [showLinkedInMockup, setShowLinkedInMockup] = useState(true);
  const [showSafeZone, setShowSafeZone] = useState(false);

  const currentPreset = MOTTO_PRESETS[presetIdx] || MOTTO_PRESETS[0];

  if (isBannerOnly) {
    return (
      <div className="m-0 p-0 w-[1584px] h-[396px] overflow-hidden bg-deep-twilight">
        <LinkedInBanner
          motto={currentPreset.motto}
          subtitle={currentPreset.subtitle}
          showSafeZoneGuide={false}
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#020330] text-white py-8 px-6 flex flex-col items-center gap-8">
      {/* Top Control Header */}
      <div className="w-full max-w-[1584px] flex flex-wrap items-center justify-between gap-4 border-b border-sky-aqua/20 pb-5">
        <div>
          <div className="flex items-center gap-2.5">
            <h1 className="text-2xl font-bold tracking-tight text-white">
              LinkedIn Banner Studio — Andrés Herencia
            </h1>
            <Badge className="bg-turquoise-surf text-deep-twilight font-semibold">
              shadcn/ui + Roboto
            </Badge>
          </div>
          <p className="text-sm text-frosted-blue/80 mt-1">
            Exact 1584 × 396 px LinkedIn cover dimensions matched to your LaTeX CV & color palette
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          {MOTTO_PRESETS.map((preset, idx) => (
            <Button
              key={preset.label}
              variant={presetIdx === idx ? "default" : "outline"}
              size="sm"
              onClick={() => setPresetIdx(idx)}
              className={
                presetIdx === idx
                  ? "bg-turquoise-surf text-deep-twilight hover:bg-sky-aqua font-semibold"
                  : "border-sky-aqua/40 text-light-cyan hover:bg-french-blue/60"
              }
            >
              <Sparkles className="w-3.5 h-3.5" />
              {preset.label}
            </Button>
          ))}

          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowSafeZone((v) => !v)}
            className="border-sky-aqua/40 text-light-cyan hover:bg-french-blue/60"
          >
            <Eye className="w-3.5 h-3.5" />
            {showSafeZone ? "Hide Safe Zone" : "Avatar Safe Zone"}
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={() => setShowLinkedInMockup((v) => !v)}
            className="border-sky-aqua/40 text-light-cyan hover:bg-french-blue/60"
          >
            {showLinkedInMockup ? "Hide Profile Mockup" : "Show Profile Mockup"}
          </Button>
        </div>
      </div>

      {/* Standalone 1584x396 Banner Canvas (For direct 1:1 export) */}
      <div className="flex flex-col items-center gap-2">
        <div className="w-[1584px] flex items-center justify-between text-xs text-frosted-blue/75 px-1">
          <span>1:1 Banner Canvas (1584 × 396 px)</span>
          <span>Font: Roboto • Theme: Deep Twilight to Bright Teal Blue</span>
        </div>
        <div className="rounded-lg overflow-hidden shadow-2xl border border-sky-aqua/30">
          <LinkedInBanner
            motto={currentPreset.motto}
            subtitle={currentPreset.subtitle}
            showSafeZoneGuide={showSafeZone}
          />
        </div>
      </div>

      {/* Live LinkedIn Profile Header Mockup with attached Profile Photo */}
      {showLinkedInMockup && (
        <Card className="w-[1584px] bg-[#0a1128] border-sky-aqua/25 overflow-hidden shadow-2xl">
          <CardHeader className="py-3 px-5 border-b border-sky-aqua/15 bg-deep-twilight/40 flex flex-row items-center justify-between">
            <div>
              <CardTitle className="text-sm font-medium text-frosted-blue">
                LinkedIn Profile Preview (with your attached profile photo)
              </CardTitle>
              <CardDescription className="text-xs text-frosted-blue/60">
                Verifies that the left-side profile picture never overlaps your name, motto, email, or AWS badges
              </CardDescription>
            </div>
            <Badge variant="outline" className="text-xs border-turquoise-surf/40 text-sky-aqua">
              Safe-Zone Verified
            </Badge>
          </CardHeader>
          <CardContent className="p-0">
            <div className="relative">
              <LinkedInBanner
                motto={currentPreset.motto}
                subtitle={currentPreset.subtitle}
                showSafeZoneGuide={false}
              />
              {/* LinkedIn Circular Avatar Overlay */}
              <div className="absolute left-[48px] -bottom-[76px] z-20">
                <Avatar className="w-[240px] h-[240px] border-[6px] border-[#0a1128] shadow-2xl">
                  <AvatarImage src="/assets/profile.jpg" alt="Andrés Herencia" />
                  <AvatarFallback className="bg-french-blue text-white text-4xl font-bold">
                    AH
                  </AvatarFallback>
                </Avatar>
              </div>
            </div>

            {/* Simulated LinkedIn Profile Lower Card */}
            <div className="pt-[92px] pb-6 px-12 bg-[#0a1128] text-white flex items-start justify-between">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <h2 className="text-2xl font-bold text-white">Andrés Herencia</h2>
                  <Badge className="bg-bright-teal-blue/40 text-light-cyan border border-sky-aqua/30 text-xs">
                    2x AWS Certified
                  </Badge>
                </div>
                <p className="text-base text-frosted-blue-2">
                  Forward Deployed AI Engineer @ Moody's Corporation (InnoIT) | M.Sc. Statistics & Data Science
                </p>
                <p className="text-xs text-frosted-blue/70">
                  Madrid, Community of Madrid, Spain • andresherencia2000@gmail.com
                </p>
              </div>
              <div className="text-right text-sm text-frosted-blue/90 space-y-1">
                <div className="font-medium text-white">InnoIT @ Moody's Corporation</div>
                <div className="text-xs text-frosted-blue/70">
                  Universidad Complutense de Madrid & UPM
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Color Palette Verification Strip */}
      <Card className="w-[1584px] bg-deep-twilight/40 border-sky-aqua/20">
        <CardContent className="py-4 px-6 flex items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-sm font-medium text-light-cyan shrink-0">
            <Palette className="w-4 h-4 text-turquoise-surf" />
            <span>Custom Palette Variables:</span>
          </div>
          <div className="flex items-center gap-3 flex-wrap justify-end">
            {PALETTE_SWATCHES.map((swatch) => (
              <div
                key={swatch.name}
                className="flex items-center gap-2 px-2.5 py-1 rounded-md bg-deep-twilight/70 border border-sky-aqua/20 text-xs"
              >
                <span
                  className="w-3.5 h-3.5 rounded-sm border border-white/20 shrink-0"
                  style={{ backgroundColor: swatch.hex }}
                />
                <span className="font-mono text-frosted-blue-2">{swatch.name}</span>
                <Check className="w-3 h-3 text-turquoise-surf" />
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default App;
