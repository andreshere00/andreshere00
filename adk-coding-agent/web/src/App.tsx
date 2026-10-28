import { useCallback, useEffect, useState, type ReactNode } from 'react'
import { ChatPanel } from '@/components/chat-panel'
import { Hero } from '@/components/hero'
import { KeyFigures } from '@/components/key-figures'
import { MemorySection } from '@/components/memory-section'
import { SiteFooter } from '@/components/site-footer'
import { SiteHeader } from '@/components/site-header'
import { SkillsSection } from '@/components/skills-section'
import { WorkspacePanel } from '@/components/workspace-panel'
import { api, type Status } from '@/lib/api'

function Section({ id, title, intro, children }: { id: string; title: string; intro: string; children: ReactNode }) {
  return (
    <section id={id} className="module section flex flex-col gap-6 md:gap-8">
      <div className="flex flex-col gap-3">
        <h2 className="heading-lg">{title}</h2>
        <p className="max-w-[60ch] text-lg">{intro}</p>
      </div>
      {children}
    </section>
  )
}

export default function App() {
  const [status, setStatus] = useState<Status | null>(null)
  const [activity, setActivity] = useState(0)

  useEffect(() => {
    api.status().then(setStatus).catch(() => {})
  }, [activity])
  const onActivity = useCallback(() => setActivity((count) => count + 1), [])

  return (
    <>
      <SiteHeader />
      <main className="pt-(--header-height)">
        <Hero />
        <KeyFigures status={status} />
        {status && !status.llm_configured && (
          <p className="module bg-orange/10 py-3 font-mono text-sm text-navy">
            OPENROUTER_API_KEY is not set. Chat will fail until you add it to .env and restart the server.
          </p>
        )}
        <Section id="chat" title="Chat" intro="Ask for code, document edits or comparisons. Tool calls are shown as they run in the sandbox.">
          <ChatPanel onActivity={onActivity} />
        </Section>
        <Section id="workspace" title="Workspace" intro="Everything the agent reads and writes lives in one jailed folder.">
          <WorkspacePanel refreshKey={activity} />
        </Section>
        <Section id="skills" title="Skills repository" intro="Local skills plus pinned third-party skills such as Anthropic's docx. Skills load on demand.">
          <SkillsSection />
        </Section>
        <Section id="memory" title="Memory" intro="Finished turns are indexed into long-term memory and recalled in later sessions.">
          <MemorySection />
        </Section>
      </main>
      <SiteFooter model={status?.model} />
    </>
  )
}
