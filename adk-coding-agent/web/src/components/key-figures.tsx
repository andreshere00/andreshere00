import type { Status } from '@/lib/api'

type Props = { status: Status | null }

function Figure({ label, value }: { label: string; value: string | number | undefined }) {
  return (
    <div className="flex items-center justify-between gap-8 border-t border-white/25 py-6 md:py-7 lg:py-8">
      <p className="text-xl text-white md:text-2xl">{label}</p>
      <p className="text-5xl font-light text-white md:text-[92px] lg:text-[96px]" style={{ lineHeight: 1 }}>
        {value ?? '–'}
      </p>
    </div>
  )
}

export function KeyFigures({ status }: Props) {
  return (
    <section className="bg-cool-gray-02">
      <div className="module section">
        <h2 className="heading-lg mb-4 text-white md:mb-6">Workspace at a glance</h2>
        <p className="mb-6 max-w-[60ch] text-xl text-white/80 md:mb-8 md:text-2xl">
          Running on <span className="font-mono uppercase text-orange">{status?.sandbox ?? '…'}</span>{' '}
          sandbox with <span className="font-mono">{status?.model ?? '…'}</span>
        </p>
        <Figure label="Skills available" value={status?.skills} />
        <Figure label="Workspace files" value={status?.files} />
        <Figure label="Saved sessions" value={status?.sessions} />
        <div className="border-t border-white/25" />
      </div>
    </section>
  )
}
