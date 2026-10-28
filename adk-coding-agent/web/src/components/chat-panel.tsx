import { ArrowRight, Plus } from 'lucide-react'
import { useCallback, useEffect, useRef, useState } from 'react'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { api, streamChat, type ChatItem, type SessionInfo } from '@/lib/api'

const SUGGESTIONS = [
  'Write fizzbuzz in fizz.py and run it',
  'What changed between plan.v1.docx and plan.v2.docx?',
  'Create a one-page Word report called summary.docx',
]

type Props = { onActivity: () => void }

function RichText({ text }: { text: string }) {
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

function Turn({ item }: { item: ChatItem }) {
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

export function ChatPanel({ onActivity }: Props) {
  const [items, setItems] = useState<ChatItem[]>([])
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [sessions, setSessions] = useState<SessionInfo[]>([])
  const [draft, setDraft] = useState('')
  const [busy, setBusy] = useState(false)
  const bottom = useRef<HTMLDivElement>(null)

  const refreshSessions = useCallback(() => api.sessions().then(setSessions).catch(() => {}), [])
  useEffect(() => {
    refreshSessions()
  }, [refreshSessions])
  useEffect(() => {
    bottom.current?.scrollIntoView({ block: 'end' })
  }, [items])

  const openSession = async (id: string) => {
    setSessionId(id)
    setItems(await api.history(id))
  }

  const newSession = () => {
    setSessionId(null)
    setItems([])
  }

  const send = async (text: string) => {
    const message = text.trim()
    if (!message || busy) return
    setDraft('')
    setBusy(true)
    setItems((current) => [...current, { kind: 'message', role: 'user', text: message }])
    try {
      await streamChat(sessionId, message, (event) => {
        if (event.kind === 'session') setSessionId(event.session_id)
        else if (event.kind !== 'done') setItems((current) => [...current, event])
      })
    } catch (error) {
      setItems((current) => [...current, { kind: 'error', text: String(error) }])
    } finally {
      setBusy(false)
      refreshSessions()
      onActivity()
    }
  }

  return (
    <div className="grid min-h-[560px] border border-warm-gray-02 grid-cols-[minmax(0,1fr)] lg:h-[72vh] lg:grid-cols-[260px_minmax(0,1fr)]">
      <aside className="hidden flex-col border-r border-warm-gray-02 bg-warm-gray-01 lg:flex">
        <div className="flex items-center justify-between px-4 py-3">
          <span className="eyebrow">Sessions</span>
          <Button variant="ghost" size="icon-xs" onClick={newSession} aria-label="New session">
            <Plus />
          </Button>
        </div>
        <ul className="flex-1 overflow-y-auto">
          {sessions.map((session) => (
            <li key={session.id} className="list-none">
              <button
                onClick={() => openSession(session.id)}
                className={`w-full px-4 py-3 text-left font-mono text-sm hover:bg-warm-gray-02 ${
                  session.id === sessionId ? 'bg-warm-gray-02 text-navy' : 'text-steel'
                }`}
              >
                {session.id}
              </button>
            </li>
          ))}
          {sessions.length === 0 && <li className="list-none px-4 py-3 text-sm text-steel">No sessions yet.</li>}
        </ul>
      </aside>

      <div className="flex min-h-0 min-w-0 flex-col">
        <div className="flex-1 overflow-y-auto p-4 md:p-6">
          {items.length === 0 ? (
            <div className="flex h-full flex-col justify-center gap-2">
              <h3 className="heading-lg mb-4">What should we build?</h3>
              {SUGGESTIONS.map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => send(suggestion)}
                  className="group hairline flex items-center justify-between gap-4 py-4 text-left text-lg text-navy hover:text-orange"
                >
                  {suggestion}
                  <ArrowRight className="size-5 shrink-0 transition-transform group-hover:translate-x-1" />
                </button>
              ))}
            </div>
          ) : (
            <div className="flex flex-col gap-6">
              {items.map((item, index) => (
                <Turn key={index} item={item} />
              ))}
              {busy && <span className="eyebrow animate-pulse text-orange">Working…</span>}
              <div ref={bottom} />
            </div>
          )}
        </div>
        <form
          className="flex items-end gap-3 border-t border-warm-gray-02 p-3 md:p-4"
          onSubmit={(event) => {
            event.preventDefault()
            send(draft)
          }}
        >
          <Textarea
            value={draft}
            onChange={(event) => setDraft(event.target.value)}
            onKeyDown={(event) => {
              if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault()
                send(draft)
              }
            }}
            placeholder="Ask the agent to write, run, edit or compare…"
            rows={2}
            className="min-h-12 flex-1 resize-none border-warm-gray-02 bg-background text-base"
          />
          <Button type="submit" size="lg" disabled={busy || !draft.trim()}>
            Send
            <ArrowRight />
          </Button>
        </form>
      </div>
    </div>
  )
}
