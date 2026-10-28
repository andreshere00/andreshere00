import type { Compare } from '@/lib/api'

function Figure({ label, value, accent }: { label: string; value: number; accent: string }) {
  return (
    <div className="flex flex-col gap-2 border-t border-white/25 py-4 md:py-5">
      <p className={`font-mono text-xs uppercase tracking-wider ${accent}`}>{label}</p>
      <p className="text-5xl font-light text-white md:text-6xl" style={{ lineHeight: 1 }}>
        {value}
      </p>
    </div>
  )
}

export function DiffStats({ compare }: { compare: Compare }) {
  const { changed, added, removed } = compare.stats
  return (
    <div className="grid grid-cols-3 gap-4 bg-cool-gray-02 px-4 pb-2 md:gap-8 md:px-6">
      <Figure label="Changed" value={changed} accent="text-orange" />
      <Figure label="Added" value={added} accent="text-diff-add-strong" />
      <Figure label="Removed" value={removed} accent="text-diff-del-strong" />
    </div>
  )
}
