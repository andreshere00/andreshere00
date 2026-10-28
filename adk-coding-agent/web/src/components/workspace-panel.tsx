import { RefreshCw } from 'lucide-react'
import { useCallback, useEffect, useState } from 'react'
import { Button } from '@/components/ui/button'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Skeleton } from '@/components/ui/skeleton'
import { api, formatBytes, type FileContent, type WorkspaceFile } from '@/lib/api'

export function WorkspacePanel({ refreshKey }: { refreshKey: number }) {
  const [files, setFiles] = useState<WorkspaceFile[] | null>(null)
  const [selected, setSelected] = useState<string | null>(null)
  const [content, setContent] = useState<FileContent | null>(null)

  const load = useCallback(() => api.files().then(setFiles).catch(() => setFiles([])), [])
  useEffect(() => {
    load()
  }, [load, refreshKey])
  useEffect(() => {
    if (selected) api.file(selected).then(setContent).catch(() => setContent(null))
  }, [selected, refreshKey])

  return (
    <div className="grid min-h-[420px] border border-warm-gray-02 grid-cols-[minmax(0,1fr)] md:grid-cols-[320px_minmax(0,1fr)]">
      <div className="flex min-h-0 flex-col border-b border-warm-gray-02 md:border-r md:border-b-0">
        <div className="flex items-center justify-between bg-warm-gray-01 px-4 py-3">
          <span className="eyebrow">Files</span>
          <Button variant="ghost" size="icon-xs" onClick={load} aria-label="Refresh files">
            <RefreshCw />
          </Button>
        </div>
        <ScrollArea className="h-80 md:h-[420px]">
          {files === null && <Skeleton className="m-4 h-24" />}
          {files?.length === 0 && (
            <p className="p-4 text-sm text-steel">The workspace is empty. Ask the agent to create a file.</p>
          )}
          <ul>
            {files?.map((file) => (
              <li key={file.path} className="list-none">
                <button
                  onClick={() => setSelected(file.path)}
                  className={`hairline flex w-full items-baseline justify-between gap-3 px-4 py-3 text-left hover:bg-warm-gray-01 ${
                    file.path === selected ? 'bg-warm-gray-01' : ''
                  }`}
                >
                  <span className="truncate font-mono text-sm text-navy">{file.path}</span>
                  <span className="shrink-0 text-xs text-steel">{formatBytes(file.size)}</span>
                </button>
              </li>
            ))}
          </ul>
        </ScrollArea>
      </div>
      <div className="min-w-0 p-4 md:p-6">
        {!selected && <p className="text-steel">Select a file to preview it.</p>}
        {selected && content?.text === null && (
          <p className="text-steel">
            <span className="font-mono text-navy">{selected}</span> is a binary file ({formatBytes(content.size)}).
            Ask the agent to inspect or compare it.
          </p>
        )}
        {selected && content?.text != null && (
          <>
            <p className="eyebrow mb-3">{content.path}</p>
            <pre className="max-h-[360px] overflow-auto bg-warm-gray-01 p-4 font-mono text-sm text-charcoal">
              {content.text}
            </pre>
          </>
        )}
      </div>
    </div>
  )
}
