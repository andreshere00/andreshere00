import { FileText, Upload } from 'lucide-react'
import { useRef, useState } from 'react'
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select'
import { api, formatBytes, type DocFile } from '@/lib/api'

type Props = {
  label: string
  value: string | null
  documents: DocFile[]
  onChange: (path: string) => void
  onUploaded: () => void
}

export function DocumentSlot({ label, value, documents, onChange, onUploaded }: Props) {
  const input = useRef<HTMLInputElement>(null)
  const [dragging, setDragging] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const current = documents.find((doc) => doc.path === value)

  const upload = async (file: File | undefined) => {
    if (!file) return
    setError(null)
    try {
      const saved = await api.upload(file)
      onUploaded()
      onChange(saved.path)
    } catch (failure) {
      setError(failure instanceof Error ? failure.message : String(failure))
    }
  }

  return (
    <div className="flex min-w-0 flex-col gap-3">
      <span className="eyebrow">{label}</span>
      <div
        onDragOver={(event) => {
          event.preventDefault()
          setDragging(true)
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(event) => {
          event.preventDefault()
          setDragging(false)
          upload(event.dataTransfer.files[0])
        }}
        className={`flex min-h-28 flex-col justify-between gap-4 border border-dashed p-4 transition-colors ${
          dragging ? 'border-orange bg-orange/5' : 'border-warm-gray-02 bg-warm-gray-01'
        }`}
      >
        <div className="flex items-start gap-3">
          <FileText className="mt-0.5 size-6 shrink-0 text-orange" />
          <div className="min-w-0">
            <p className="truncate text-lg text-navy" data-testid={`${label}-name`}>
              {current ? current.path : 'No document selected'}
            </p>
            <p className="font-mono text-xs text-steel">
              {current ? formatBytes(current.size) : 'Drop a .docx here or upload one'}
            </p>
          </div>
        </div>
        <div className="flex flex-wrap items-center gap-3">
          <Select value={value ?? ''} onValueChange={(next) => next && onChange(next)}>
            <SelectTrigger size="sm" className="min-w-0 max-w-full flex-1 bg-white" aria-label={`${label} document`}>
              <SelectValue placeholder="Choose from workspace" />
            </SelectTrigger>
            <SelectContent>
              {documents.map((doc) => (
                <SelectItem key={doc.path} value={doc.path}>
                  {doc.path}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
          <button
            type="button"
            onClick={() => input.current?.click()}
            className="eyebrow inline-flex items-center gap-2 py-1 hover:text-orange"
          >
            <Upload className="size-4" />
            Upload
          </button>
          <input
            ref={input}
            type="file"
            accept=".docx,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            className="hidden"
            data-testid={`${label}-file`}
            onChange={(event) => {
              upload(event.target.files?.[0])
              event.target.value = ''
            }}
          />
        </div>
      </div>
      {error && <p className="border-l-2 border-destructive pl-3 font-mono text-sm text-destructive">{error}</p>}
    </div>
  )
}
