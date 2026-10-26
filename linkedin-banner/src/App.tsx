import { useState } from "react";
import { LinkedInBanner } from "@/components/LinkedInBanner";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Eye, Sparkles } from "lucide-react";

const MOTTO_PRESETS = [
  {
    label: "Forward Deployed AI Engineer",
    motto: "Forward Deployed AI Engineer",
  },
  {
    label: "ML Engineer & AI Solutions Architect",
    motto: "Machine Learning Engineer & AI Solutions Architect",
  },
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
          showSafeZoneGuide={false}
        />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#020330] text-white py-8 px-6 flex flex-col items-center gap-8">
      {/* Minimal Top Toolbar */}
      <div className="w-full max-w-[1584px] flex flex-wrap items-center justify-between gap-4">
        <h1 className="text-xl font-bold tracking-tight text-white">
          LinkedIn Banner (1584 × 396 px)
        </h1>

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
            {showLinkedInMockup ? "Hide Profile Preview" : "Show Profile Preview"}
          </Button>
        </div>
      </div>

      {/* Standalone 1584x396 Banner Canvas */}
      <div className="rounded-lg overflow-hidden shadow-2xl border border-sky-aqua/30">
        <LinkedInBanner
          motto={currentPreset.motto}
          showSafeZoneGuide={showSafeZone}
        />
      </div>

      {/* Live LinkedIn Profile Header Mockup with attached Profile Photo */}
      {showLinkedInMockup && (
        <Card className="w-[1584px] bg-[#0a1128] border-sky-aqua/25 overflow-hidden shadow-2xl">
          <CardContent className="p-0">
            <div className="relative">
              <LinkedInBanner
                motto={currentPreset.motto}
                showSafeZoneGuide={false}
              />
              <div className="absolute left-[48px] -bottom-[76px] z-20">
                <Avatar className="w-[240px] h-[240px] border-[6px] border-[#0a1128] shadow-2xl">
                  <AvatarImage src="/assets/profile.jpg" alt="Andrés Herencia" />
                  <AvatarFallback className="bg-french-blue text-white text-4xl font-bold">
                    AH
                  </AvatarFallback>
                </Avatar>
              </div>
            </div>

            <div className="pt-[92px] pb-6 px-12 bg-[#0a1128] text-white flex items-start justify-between">
              <div className="space-y-1">
                <h2 className="text-2xl font-bold text-white">Andrés Herencia</h2>
                <p className="text-base text-frosted-blue-2">
                  Forward Deployed AI Engineer @ Moody's Corporation (InnoIT) | 2x AWS-Certified
                </p>
                <p className="text-sm text-frosted-blue/70">
                  Madrid, Spain • andresherencia2000@gmail.com
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}

export default App;
