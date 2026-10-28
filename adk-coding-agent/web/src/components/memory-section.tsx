import { ArrowRight } from 'lucide-react'
import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { api, type MemoryEntry } from '@/lib/api'

export function MemorySection() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<MemoryEntry[] | null>(null)

  const search = async () => {
    if (query.trim()) setResults(await api.memory(query.trim()))
  }

  return (
    <div className="flex flex-col gap-8">
      <form
        className="flex max-w-2xl flex-col gap-3 sm:flex-row"
        onSubmit={(event) => {
          event.preventDefault()
          search()
        }}
      >
        <Input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Search what the agent remembers…"
          className="h-11 flex-1 border-warm-gray-02 text-base"
        />
        <Button type="submit">
          Search
          <ArrowRight />
        </Button>
      </form>
      {results?.length === 0 && <p className="text-steel">Nothing found for “{query}”.</p>}
      <div className="grid gap-2 md:grid-cols-2">
        {results?.map((entry, index) => (
          <blockquote key={index} className="flex gap-8 py-6">
            <span className="w-0 self-stretch border-l-2 border-orange" />
            <div className="flex flex-col gap-4">
              <p className="line-clamp-6 text-lg text-navy md:text-xl">“{entry.text}”</p>
              <cite className="text-sm not-italic">
                {entry.author ?? 'unknown'}
                {entry.timestamp ? ` · ${new Date(entry.timestamp).toLocaleString()}` : ''}
              </cite>
            </div>
          </blockquote>
        ))}
      </div>
    </div>
  )
}
