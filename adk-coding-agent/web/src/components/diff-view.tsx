import { Fragment, useMemo } from 'react'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import type { Compare, DiffLine, Hunk, Segment } from '@/lib/api'

const ROW = {
  context: 'bg-white text-navy',
  delete: 'bg-diff-del text-navy',
  insert: 'bg-diff-add text-navy',
} as const
const SIGN = { context: ' ', delete: '-', insert: '+' } as const

function Text({ line }: { line: DiffLine }) {
  if (!line.segments?.length) return <>{line.text || ' '}</>
  const strong = line.type === 'delete' ? 'bg-diff-del-strong' : 'bg-diff-add-strong'
  return (
    <>
      {line.segments.map((segment: Segment, index) => (
        <span key={index} className={segment.kind === 'equal' ? undefined : strong}>
          {segment.text}
        </span>
      ))}
    </>
  )
}

function Gutter({ value }: { value: number | null }) {
  return (
    <span className="w-10 shrink-0 select-none px-2 text-right text-steel/70">{value ?? ''}</span>
  )
}

function UnifiedHunk({ hunk }: { hunk: Hunk }) {
  return (
    <div className="font-mono text-[13px] leading-6">
      <div className="bg-light-gray px-3 py-1 text-xs text-steel">
        @@ -{hunk.old_start},{hunk.old_count} +{hunk.new_start},{hunk.new_count} @@
      </div>
      {hunk.lines.map((line, index) => (
        <div key={index} className={`flex ${ROW[line.type]}`} data-line={line.type}>
          <Gutter value={line.old_no} />
          <Gutter value={line.new_no} />
          <span className="w-5 shrink-0 select-none text-center text-steel">{SIGN[line.type]}</span>
          <span className="min-w-0 flex-1 whitespace-pre-wrap break-words pr-3">
            <Text line={line} />
          </span>
        </div>
      ))}
    </div>
  )
}

type Pair = { left: DiffLine | null; right: DiffLine | null }

function pairLines(lines: DiffLine[]): Pair[] {
  const pairs: Pair[] = []
  let index = 0
  while (index < lines.length) {
    const line = lines[index]
    if (line.type === 'context') {
      pairs.push({ left: line, right: line })
      index += 1
      continue
    }
    const deleted: DiffLine[] = []
    const inserted: DiffLine[] = []
    while (index < lines.length && lines[index].type !== 'context') {
      ;(lines[index].type === 'delete' ? deleted : inserted).push(lines[index])
      index += 1
    }
    for (let row = 0; row < Math.max(deleted.length, inserted.length); row += 1) {
      pairs.push({ left: deleted[row] ?? null, right: inserted[row] ?? null })
    }
  }
  return pairs
}

function Cell({ line, side }: { line: DiffLine | null; side: 'old' | 'new' }) {
  if (!line) return <div className="bg-light-gray/60" />
  return (
    <div className={`flex min-w-0 ${ROW[line.type]}`}>
      <Gutter value={side === 'old' ? line.old_no : line.new_no} />
      <span className="min-w-0 flex-1 whitespace-pre-wrap break-words pr-3">
        <Text line={line} />
      </span>
    </div>
  )
}

function SplitHunk({ hunk }: { hunk: Hunk }) {
  const pairs = useMemo(() => pairLines(hunk.lines), [hunk])
  return (
    <div className="font-mono text-[13px] leading-6">
      <div className="bg-light-gray px-3 py-1 text-xs text-steel">
        @@ -{hunk.old_start},{hunk.old_count} +{hunk.new_start},{hunk.new_count} @@
      </div>
      <div className="grid grid-cols-[minmax(0,1fr)_minmax(0,1fr)] gap-x-px bg-warm-gray-02">
        {pairs.map((pair, index) => (
          <Fragment key={index}>
            <Cell line={pair.left} side="old" />
            <Cell line={pair.right} side="new" />
          </Fragment>
        ))}
      </div>
    </div>
  )
}

function Hunks({ compare, split }: { compare: Compare; split: boolean }) {
  return (
    <div className="flex flex-col border border-warm-gray-02">
      {compare.hunks.map((hunk, index) => {
        const previous = compare.hunks[index - 1]
        const skipped = hunk.old_start - 1 - (previous ? previous.old_start - 1 + previous.old_count : 0)
        return (
          <Fragment key={index}>
            {skipped > 0 && (
              <div className="bg-warm-gray-01 px-3 py-1.5 text-center font-mono text-xs text-steel">
                ⋯ {skipped} unchanged {skipped === 1 ? 'block' : 'blocks'}
              </div>
            )}
            {split ? <SplitHunk hunk={hunk} /> : <UnifiedHunk hunk={hunk} />}
          </Fragment>
        )
      })}
    </div>
  )
}

export function DiffView({ compare }: { compare: Compare }) {
  if (compare.hunks.length === 0) {
    return (
      <p className="border border-warm-gray-02 bg-warm-gray-01 p-6 text-lg text-navy">
        The two documents have identical content.
      </p>
    )
  }
  return (
    <Tabs defaultValue="unified" className="gap-4">
      <TabsList>
        <TabsTrigger value="unified">Unified</TabsTrigger>
        <TabsTrigger value="split">Split</TabsTrigger>
      </TabsList>
      <TabsContent value="unified">
        <Hunks compare={compare} split={false} />
      </TabsContent>
      <TabsContent value="split">
        <Hunks compare={compare} split />
      </TabsContent>
    </Tabs>
  )
}
