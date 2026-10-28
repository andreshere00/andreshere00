import type { ChatItem } from '@/lib/api'

export function RichText({ text }: { text: string }) {
  return (
    <div className="flex flex-col gap-3">
      {text.split(/```/).map((chunk, index) =>
        index % 2 === 1 ? (
          <pre key={index} className="max-w-full overflow-x-auto bg-warm-gray-01 p-4 font-mono text-sm leading-relaxed text-navy">
            {chunk.replace(/^\w*\n/, '').trimEnd()}
          </pre>
        ) : (
          chunk.trim() && (
            <p key={index} className="whitespace-pre-wrap break-words text-navy">
              {chunk.trim()}
            </p>
          )
        ),
      )}
    </div>
  )
}

function ToolRow({ item }: { item: Extract<ChatItem, { kind: 'tool_call' | 'tool_result' }> }) {
  const isCall = item.kind === 'tool_call'
  const payload = isCall ? item.args : item.response
  const summary = isCall ? String(item.args.command ?? item.args.path ?? item.args.skill_name ?? '') : ''
  const failed = !isCall && (item.response.status === 'error' || Boolean(item.response.error))
  return (
    <details className="group border-l-2 border-orange pl-4">
      <summary className="flex cursor-pointer list-none flex-wrap items-baseline gap-x-3 py-1">
        <span className="eyebrow">{isCall ? 'Tool' : failed ? 'Failed' : 'Result'}</span>
        <span className="font-mono text-sm text-navy">{item.name}</span>
        {summary && <span className="truncate font-mono text-sm text-steel">{summary}</span>}
      </summary>
      <pre className="mt-2 max-h-72 overflow-auto bg-warm-gray-01 p-3 font-mono text-xs text-charcoal">
        {JSON.stringify(payload, null, 2)}
      </pre>
    </details>
  )
}

export function Turn({ item }: { item: ChatItem }) {
  if (item.kind === 'tool_call' || item.kind === 'tool_result') return <ToolRow item={item} />
  if (item.kind === 'error') {
    return <p className="border-l-2 border-destructive pl-4 font-mono text-sm text-destructive">{item.text}</p>
  }
  return (
    <div className="flex flex-col gap-2">
      <span className="eyebrow text-steel">{item.role === 'user' ? 'You' : 'Agent'}</span>
      <RichText text={item.text} />
    </div>
  )
}
