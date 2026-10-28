import { useEffect, useState } from 'react'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import { api, type Skill } from '@/lib/api'

function SkillCard({ skill }: { skill: Skill }) {
  return (
    <article className="group flex flex-col gap-3">
      <div className="aspect-video overflow-hidden bg-warm-gray-01">
        <div className="flex size-full items-end p-5 transition-transform duration-500 ease-out group-hover:scale-[1.07]">
          <span className="font-mono text-2xl uppercase text-navy md:text-3xl">{skill.name}</span>
        </div>
      </div>
      <div className="flex items-center gap-2">
        <Badge variant={skill.source === 'local' ? 'default' : 'outline'}>{skill.source}</Badge>
        <span className="w-px self-stretch bg-warm-gray-02" />
        <span className="text-base text-cool-gray-02">SKILL.md</span>
      </div>
      <h3 className="text-xl text-navy">{skill.name}</h3>
      <p className="line-clamp-4 text-base">{skill.description}</p>
    </article>
  )
}

export function SkillsSection() {
  const [skills, setSkills] = useState<Skill[] | null>(null)
  useEffect(() => {
    api.skills().then(setSkills).catch(() => setSkills([]))
  }, [])

  return (
    <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 lg:gap-6">
      {skills === null && [0, 1, 2].map((key) => <Skeleton key={key} className="aspect-video" />)}
      {skills?.map((skill) => <SkillCard key={skill.name} skill={skill} />)}
    </div>
  )
}
