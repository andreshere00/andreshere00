import { ArrowRight } from 'lucide-react'
import { useEffect, useRef, useState } from 'react'
import { Turn } from '@/components/chat-parts'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { streamAsk, type ChatItem } from '@/lib/api'

const SUGGESTIONS = [
  'Summarise the changes in plain language',
  'Did any numbers or dates change?',
  'Which changes could have legal or financial impact?',
  'List everything that was removed',
]

type Props = { oldName: string; newName: string; onActivity: () => void }

export function AskPanel({ oldName, newName, onActivity }: Props) {
  const [items, setItems] = useState<ChatItem[]>([])
  const [sessionId, setSessionId] = useState<string | null>(null)
  const [draft, setDraft] = useState('')
  const [busy, setBusy] = useState(false)
  const bottom = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottom.current?.scrollIntoView({ block: 'nearest' })
  }, [items])

  const send = async (text: string) => {
    const question = text.trim()
    if (!question || busy) return
    setDraft('')
    setBusy(true)
    setItems((current) => [...current, { kind: 'message', role: 'user', text: question }])
    try {
      await streamAsk({ old: oldName, new: newName, question, session_id: sessionId }, (event) => {
        if (event.kind === 'session') setSessionId(event.session_id)
        else if (event.kind !== 'done') setItems((current) => [...current, event])
      })
    } catch (error) {
      setItems((current) => [...current, { kind: 'error', text: String(error instanceof Error ? error.message : error) }])
    } finally {
      setBusy(false)
      onActivity()
    }
  }

  return (
    <div className="flex min-h-[480px] min-w-0 flex-col border border-warm-gray-02 lg:sticky lg:top-[calc(var(--header-height)+16px)] lg:h-[calc(100vh-var(--header-height)-32px)] lg:max-h-[760px]">
      <div className="flex-1 overflow-y-auto p-4 md:p-6">
        {items.length === 0 ? (
          <div className="flex h-full flex-col justify-center gap-1">
            <h3 className="heading-lg mb-4">Ask about these documents</h3>
            {SUGGESTIONS.map((suggestion) => (
              <button
                key={suggestion}
                onClick={() => send(suggestion)}
                className="group hairline flex items-center justify-between gap-4 py-3 text-left text-base text-navy hover:text-orange"
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
            {busy && <span className="eyebrow animate-pulse text-orange">Reading…</span>}
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
          placeholder="Ask a question about the content…"
          rows={2}
          className="min-h-12 flex-1 resize-none border-warm-gray-02 bg-background text-base"
        />
        <Button type="submit" size="lg" disabled={busy || !draft.trim()}>
          Ask
          <ArrowRight />
        </Button>
      </form>
    </div>
  )
}
