import { ArrowLeftRight } from 'lucide-react'
import { useCallback, useEffect, useState } from 'react'
import { AskPanel } from '@/components/ask-panel'
import { DiffStats } from '@/components/diff-stats'
import { DiffView } from '@/components/diff-view'
import { DocumentSlot } from '@/components/document-slot'
import { Button } from '@/components/ui/button'
import { Skeleton } from '@/components/ui/skeleton'
import { api, type Compare, type DocFile } from '@/lib/api'

type Props = { onActivity: () => void }

export function CompareSection({ onActivity }: Props) {
  const [documents, setDocuments] = useState<DocFile[]>([])
  const [oldName, setOldName] = useState<string | null>(null)
  const [newName, setNewName] = useState<string | null>(null)
  const [compare, setCompare] = useState<Compare | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const refresh = useCallback(() => {
    api.documents().then(setDocuments).catch(() => setDocuments([]))
  }, [])

  useEffect(() => {
    refresh()
  }, [refresh])

  useEffect(() => {
    if (!oldName || !newName) return
    const controller = new AbortController()
    setLoading(true)
    setError(null)
    api
      .compare(oldName, newName, controller.signal)
      .then((result) => {
        setCompare(result)
        setLoading(false)
      })
      .catch((failure: unknown) => {
        if (controller.signal.aborted) return
        setCompare(null)
        setError(failure instanceof Error ? failure.message : String(failure))
        setLoading(false)
      })
    return () => controller.abort()
  }, [oldName, newName])

  const swap = () => {
    setOldName(newName)
    setNewName(oldName)
  }

  return (
    <div className="flex flex-col gap-8">
      <div className="grid grid-cols-[minmax(0,1fr)] items-end gap-4 md:grid-cols-[minmax(0,1fr)_auto_minmax(0,1fr)]">
        <DocumentSlot label="Original" value={oldName} documents={documents} onChange={setOldName} onUploaded={refresh} />
        <Button variant="outline" size="icon-lg" onClick={swap} disabled={!oldName && !newName} aria-label="Swap documents" className="mx-auto md:mb-1">
          <ArrowLeftRight />
        </Button>
        <DocumentSlot label="Revised" value={newName} documents={documents} onChange={setNewName} onUploaded={refresh} />
      </div>

      {error && <p className="border-l-2 border-destructive pl-4 font-mono text-sm text-destructive">{error}</p>}

      {!oldName || !newName ? (
        <p className="hairline py-8 text-lg text-steel">
          Choose or upload two Word documents to see what changed between them.
        </p>
      ) : (
        <div className="grid grid-cols-[minmax(0,1fr)] gap-6 lg:grid-cols-12 lg:gap-3.5">
          <div className="flex min-w-0 flex-col gap-6 lg:col-span-7">
            {loading && !compare ? (
              <Skeleton className="h-64 w-full" />
            ) : (
              compare && (
                <>
                  <DiffStats compare={compare} />
                  <DiffView compare={compare} />
                </>
              )
            )}
          </div>
          <div className="min-w-0 lg:col-span-5">
            <AskPanel key={`${oldName}|${newName}`} oldName={oldName} newName={newName} onActivity={onActivity} />
          </div>
        </div>
      )}
    </div>
  )
}
