import { useCallback, useEffect, useState, type ReactNode } from 'react'
import { CompareSection } from '@/components/compare-section'
import { Hero } from '@/components/hero'
import { MemorySection } from '@/components/memory-section'
import { SiteFooter } from '@/components/site-footer'
import { SiteHeader } from '@/components/site-header'
import { SkillsSection } from '@/components/skills-section'
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
        {status && !status.llm_configured && (
          <p className="module bg-orange/10 py-3 font-mono text-sm text-navy">
            OPENROUTER_API_KEY is not set. Comparing works, but questions will fail until you add it to .env and restart the server.
          </p>
        )}
        <Section id="compare" title="Compare" intro="Pick two versions of a document. Changes appear like a git diff, and you can ask questions about either file.">
          <CompareSection onActivity={onActivity} />
        </Section>
        <Section id="skills" title="Skills repository" intro="The doc-diff skill powers this view. Local skills plus pinned third-party skills such as Anthropic's docx.">
          <SkillsSection />
        </Section>
        <Section id="memory" title="Memory" intro="Answers are indexed into long-term memory and recalled in later sessions.">
          <MemorySection />
        </Section>
      </main>
      <SiteFooter model={status?.model} />
    </>
  )
}
